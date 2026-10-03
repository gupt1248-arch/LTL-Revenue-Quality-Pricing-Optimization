from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="LTL Revenue Quality", layout="wide")
ROOT=Path(__file__).resolve().parents[1]

@st.cache_data
def load():
    df=pd.read_csv(ROOT/"data"/"processed"/"shipments_scored.csv.gz",parse_dates=["ship_date"])
    sim=pd.read_csv(ROOT/"data"/"processed"/"pricing_scenarios.csv")
    return df,sim

df,sim=load()
st.title("LTL Revenue Quality & Pricing Optimization")
st.caption("Synthetic portfolio case study — no confidential FedEx data.")

with st.sidebar:
    st.header("Filters")
    date_min,date_max=df.ship_date.min().date(),df.ship_date.max().date()
    dr=st.date_input("Ship date",[date_min,date_max],min_value=date_min,max_value=date_max)
    cust=st.multiselect("Customer",sorted(df.customer_name.unique()))
    service=st.multiselect("Service",sorted(df.service_level.unique()))
    flag=st.multiselect("Revenue quality flag",["Critical","High","Watch","Normal"])

f=df.copy()
if len(dr)==2:
    f=f[(f.ship_date.dt.date>=dr[0])&(f.ship_date.dt.date<=dr[1])]
if cust: f=f[f.customer_name.isin(cust)]
if service: f=f[f.service_level.isin(service)]
if flag: f=f[f.revenue_quality_flag.isin(flag)]

c1,c2,c3,c4,c5=st.columns(5)
c1.metric("Shipments",f"{f.shipment_id.nunique():,}")
c2.metric("Revenue",f"${f.billed_revenue.sum()/1e6:,.1f}M")
c3.metric("Revenue gap",f"${f.revenue_gap.sum()/1e6:,.2f}M")
c4.metric("Pricing realization",f"{f.billed_revenue.sum()/f.expected_revenue.sum():.2%}")
c5.metric("Contribution",f"${f.contribution.sum()/1e6:,.1f}M")

tab1,tab2,tab3,tab4=st.tabs(["Executive","Root Cause","Customer × Lane","Pricing Scenarios"])

with tab1:
    m=f.assign(month=f.ship_date.dt.to_period("M").astype(str)).groupby("month",as_index=False).agg(
        revenue=("billed_revenue","sum"),expected=("expected_revenue","sum"),gap=("revenue_gap","sum"))
    m["realization"]=m.revenue/m.expected
    col1,col2=st.columns(2)
    with col1:
        st.plotly_chart(px.line(m,x="month",y="realization",markers=True,title="Pricing realization trend"),use_container_width=True)
    with col2:
        top=f.groupby("customer_name",as_index=False).revenue_gap.sum().nlargest(10,"revenue_gap")
        st.plotly_chart(px.bar(top,x="revenue_gap",y="customer_name",orientation="h",title="Top customer revenue gaps"),use_container_width=True)

with tab2:
    roots=f[f.injected_issue!="None"].groupby("injected_issue",as_index=False).agg(
        shipments=("shipment_id","nunique"),revenue_gap=("revenue_gap","sum")).sort_values("revenue_gap",ascending=False)
    st.plotly_chart(px.bar(roots,x="revenue_gap",y="injected_issue",orientation="h",title="Synthetic root-cause validation"),use_container_width=True)
    st.info("`injected_issue` is synthetic ground truth for validating the analytical workflow. In production, root cause must be inferred from governed source data.")

with tab3:
    cells=f.groupby(["customer_name","lane_id"],as_index=False).agg(
        shipments=("shipment_id","nunique"),revenue=("billed_revenue","sum"),expected=("expected_revenue","sum"),
        gap=("revenue_gap","sum"),contribution=("contribution","sum"))
    cells["realization"]=cells.revenue/cells.expected
    cells=cells[cells.shipments>=30]
    st.plotly_chart(px.scatter(cells,x="shipments",y="realization",size="gap",hover_name="customer_name",
                               hover_data=["lane_id","revenue","contribution"],title="Customer × Lane prioritization"),
                    use_container_width=True)
    st.dataframe(cells.sort_values("gap",ascending=False).head(30),use_container_width=True)

with tab4:
    ss=sim.groupby("price_action",as_index=False)[["incremental_revenue","incremental_contribution"]].sum()
    ss["expected_volume_change"]=sim.groupby("price_action").expected_volume_change.mean().values
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=ss.price_action*100,y=ss.incremental_contribution/1e6,mode="lines+markers",name="Incremental contribution ($M)"))
    fig.update_layout(title="Targeted pricing scenario",xaxis_title="Price action (%)",yaxis_title="$M")
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(ss.style.format({"price_action":"{:.0%}","expected_volume_change":"{:.2%}",
                                  "incremental_revenue":"${:,.0f}","incremental_contribution":"${:,.0f}"}),use_container_width=True)
    st.warning("Elasticity is illustrative. Production recommendations require empirically estimated customer/segment elasticity and contract review.")
