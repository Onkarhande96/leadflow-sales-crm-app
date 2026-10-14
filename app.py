"""
LeadFlow CRM — Sales Pipeline & Lead Intelligence Dashboard
Engineered by Onkar Hande (BCA / MCA)
Streamlit Cloud & Enterprise Ready
"""

import io
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="LeadFlow CRM — Sales Pipeline & Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# CUSTOM STYLING (CSS)
# ==========================================
st.markdown(
    """
    <style>
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* Action Buttons */
    .wa-btn {
        display: inline-flex;
        align-items: center;
        background-color: #25D366;
        color: white !important;
        text-decoration: none;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: background 0.2s;
    }
    .wa-btn:hover {
        background-color: #128C7E;
    }

    /* Footer styling */
    .crm-footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #94a3b8;
        font-size: 0.88rem;
        border-top: 1px solid #e2e8f0;
    }
    .crm-footer a {
        color: #2563eb;
        text-decoration: none;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# DEFAULT SAMPLE DATA
# ==========================================
DEFAULT_LEADS = [
    {"Lead_ID": "LEAD-101", "Client_Name": "Amit Sharma", "Company": "Apex Logistics Pune", "Phone": "919876543210", "Email": "amit@apexlogistics.in", "Lead_Source": "Website", "Service_Required": "Excel Automation & Cleaning", "Deal_Value_INR": 35000, "Pipeline_Stage": "Deal Won", "Priority": "High", "Next_Follow_Up": "2026-10-15", "Notes": "Closed multi-depot inventory tracking workbook."},
    {"Lead_ID": "LEAD-102", "Client_Name": "Pooja Deshmukh", "Company": "Deshmukh Organic Mart", "Phone": "919823456781", "Email": "pooja@deshmukhorganic.com", "Lead_Source": "Instagram", "Service_Required": "E-Commerce Development", "Deal_Value_INR": 60000, "Pipeline_Stage": "Proposal Sent", "Priority": "High", "Next_Follow_Up": "2026-10-18", "Notes": "Sent quotation for Shopify store setup with payment gateway."},
    {"Lead_ID": "LEAD-103", "Client_Name": "Rohan Mehta", "Company": "Mehta Financial Services", "Phone": "919811223344", "Email": "rohan@mehtafin.com", "Lead_Source": "LinkedIn", "Service_Required": "n8n Workflow Automation", "Deal_Value_INR": 45000, "Pipeline_Stage": "Contacted", "Priority": "Medium", "Next_Follow_Up": "2026-10-19", "Notes": "Demo call done; interested in lead notification to Telegram."},
    {"Lead_ID": "LEAD-104", "Client_Name": "Priya Patel", "Company": "Patel Exports Surat", "Phone": "919922334455", "Email": "priya@patelexports.com", "Lead_Source": "Google Ads", "Service_Required": "Excel Automation & Cleaning", "Deal_Value_INR": 25000, "Pipeline_Stage": "Deal Won", "Priority": "Medium", "Next_Follow_Up": "2026-10-14", "Notes": "Delivered export shipment reconciler with macros."},
    {"Lead_ID": "LEAD-105", "Client_Name": "Vikram Joshi", "Company": "Joshi Auto Spares", "Phone": "919733445566", "Email": "vikram@joshiauto.in", "Lead_Source": "Referral", "Service_Required": "Power BI Dashboard", "Deal_Value_INR": 50000, "Pipeline_Stage": "Proposal Sent", "Priority": "High", "Next_Follow_Up": "2026-10-20", "Notes": "Waiting for MD approval on sales dashboard spec."},
    {"Lead_ID": "LEAD-106", "Client_Name": "Sneha Kulkarni", "Company": "Kulkarni Diagnostics", "Phone": "919855667788", "Email": "sneha@kulkarnilab.com", "Lead_Source": "Website", "Service_Required": "n8n Workflow Automation", "Deal_Value_INR": 30000, "Pipeline_Stage": "New Lead", "Priority": "High", "Next_Follow_Up": "2026-10-16", "Notes": "Wants automated patient report delivery via WhatsApp API."},
    {"Lead_ID": "LEAD-107", "Client_Name": "Rajesh Verma", "Company": "Verma Digital Agency", "Phone": "919866778899", "Email": "rajesh@vermadigital.in", "Lead_Source": "LinkedIn", "Service_Required": "Lead Generation", "Deal_Value_INR": 40000, "Pipeline_Stage": "Deal Won", "Priority": "High", "Next_Follow_Up": "2026-10-12", "Notes": "Contract signed for 200 verified B2B leads monthly."},
    {"Lead_ID": "LEAD-108", "Client_Name": "Neha Patil", "Company": "Patil Agro Mart", "Phone": "919877889900", "Email": "neha@patilagro.com", "Lead_Source": "Referral", "Service_Required": "E-Commerce Development", "Deal_Value_INR": 55000, "Pipeline_Stage": "Lost", "Priority": "Low", "Next_Follow_Up": "2026-10-10", "Notes": "Budget constrained; opted for basic social media catalog."},
    {"Lead_ID": "LEAD-109", "Client_Name": "Anand Rathi", "Company": "Rathi Builders Nashik", "Phone": "919888990011", "Email": "anand@rathibuilders.com", "Lead_Source": "Google Ads", "Service_Required": "Lead Generation", "Deal_Value_INR": 85000, "Pipeline_Stage": "Proposal Sent", "Priority": "High", "Next_Follow_Up": "2026-10-21", "Notes": "High-ticket residential project launch campaign."},
    {"Lead_ID": "LEAD-110", "Client_Name": "Kavita Nair", "Company": "Nair Wellness Center", "Phone": "919899001122", "Email": "kavita@nairwellness.in", "Lead_Source": "Instagram", "Service_Required": "n8n Workflow Automation", "Deal_Value_INR": 28000, "Pipeline_Stage": "Contacted", "Priority": "Medium", "Next_Follow_Up": "2026-10-17", "Notes": "Needs appointment reminder bot linked to Google Calendar."},
    {"Lead_ID": "LEAD-111", "Client_Name": "Sanjay Gupta", "Company": "Gupta Textiles Surat", "Phone": "919900112233", "Email": "sanjay@guptatextiles.com", "Lead_Source": "Website", "Service_Required": "Excel Automation & Cleaning", "Deal_Value_INR": 22000, "Pipeline_Stage": "New Lead", "Priority": "Medium", "Next_Follow_Up": "2026-10-16", "Notes": "Messy vendor GST reconciliation files needed within 2 days."},
    {"Lead_ID": "LEAD-112", "Client_Name": "Deepak Patil", "Company": "Deepak Engineering Kolhapur", "Phone": "919911223344", "Email": "deepak@deepakeng.co.in", "Lead_Source": "Referral", "Service_Required": "Power BI Dashboard", "Deal_Value_INR": 48000, "Pipeline_Stage": "Deal Won", "Priority": "High", "Next_Follow_Up": "2026-10-13", "Notes": "Built machine downtime and scrap monitoring report."},
    {"Lead_ID": "LEAD-113", "Client_Name": "Meera Iyer", "Company": "Iyer Consulting Mumbai", "Phone": "919922334455", "Email": "meera@iyerconsult.com", "Lead_Source": "LinkedIn", "Service_Required": "n8n Workflow Automation", "Deal_Value_INR": 65000, "Pipeline_Stage": "Proposal Sent", "Priority": "High", "Next_Follow_Up": "2026-10-22", "Notes": "Enterprise multi-step CRM lead routing system."},
    {"Lead_ID": "LEAD-114", "Client_Name": "Sunil Shinde", "Company": "Shinde Transports", "Phone": "919933445566", "Email": "sunil@shindetrans.in", "Lead_Source": "Google Ads", "Service_Required": "Excel Automation & Cleaning", "Deal_Value_INR": 18000, "Pipeline_Stage": "Contacted", "Priority": "Low", "Next_Follow_Up": "2026-10-18", "Notes": "Driver trip sheet audit and diesel expense calculator."},
    {"Lead_ID": "LEAD-115", "Client_Name": "Poonam Kale", "Company": "Kale Fashion Studio Pune", "Phone": "919944556677", "Email": "poonam@kalefashion.com", "Lead_Source": "Instagram", "Service_Required": "E-Commerce Development", "Deal_Value_INR": 38000, "Pipeline_Stage": "New Lead", "Priority": "Medium", "Next_Follow_Up": "2026-10-17", "Notes": "Inquired about boutique catalog website with Razorpay integration."},
]

# Initialize Session State
if "leads_data" not in st.session_state:
    st.session_state.leads_data = pd.DataFrame(DEFAULT_LEADS)

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("### 💼 LeadFlow CRM")
    st.caption("Sales Pipeline & Lead Intelligence SaaS")
    st.markdown("---")

    # Quick Search Filter
    search_query = st.text_input("🔍 Quick Search (Name / Company)", "")

    # Stage Filter
    stages = ["All"] + sorted(list(st.session_state.leads_data["Pipeline_Stage"].unique()))
    selected_stage = st.selectbox("📌 Filter by Stage", stages)

    # Priority Filter
    priorities = ["All"] + sorted(list(st.session_state.leads_data["Priority"].unique()))
    selected_priority = st.selectbox("⭐ Filter by Priority", priorities)

    # Lead Source Filter
    sources = ["All"] + sorted(list(st.session_state.leads_data["Lead_Source"].unique()))
    selected_source = st.selectbox("🌐 Filter by Source", sources)

    st.markdown("---")
    if st.button("🔄 Reset to Default Sample Leads", use_container_width=True):
        st.session_state.leads_data = pd.DataFrame(DEFAULT_LEADS)
        st.success("CRM reset to default sample dataset!")
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b;">
        <strong>Live SaaS Engine</strong><br>
        Built by Onkar Hande<br>
        <a href="https://onkarhande96.github.io" target="_blank" style="color: #2563eb; text-decoration: none;">View Portfolio ↗</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# FILTER LOGIC
# ==========================================
filtered_df = st.session_state.leads_data.copy()

if search_query:
    filtered_df = filtered_df[
        filtered_df["Client_Name"].str.contains(search_query, case=False, na=False)
        | filtered_df["Company"].str.contains(search_query, case=False, na=False)
    ]

if selected_stage != "All":
    filtered_df = filtered_df[filtered_df["Pipeline_Stage"] == selected_stage]

if selected_priority != "All":
    filtered_df = filtered_df[filtered_df["Priority"] == selected_priority]

if selected_source != "All":
    filtered_df = filtered_df[filtered_df["Lead_Source"] == selected_source]

# ==========================================
# HEADER
# ==========================================
col_hdr1, col_hdr2 = st.columns([3, 1])
with col_hdr1:
    st.title("💼 LeadFlow — Sales Intelligence & CRM")
    st.markdown("Monitor pipeline health, track client deal velocity, and manage sales conversions in real-time.")
with col_hdr2:
    st.markdown("<br>", unsafe_allow_html=True)
    # Quick export button
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        st.session_state.leads_data.to_excel(writer, index=False, sheet_name="Leads_CRM")
    st.download_button(
        label="📥 Export Full CRM (.xlsx)",
        data=output.getvalue(),
        file_name=f"LeadFlow_CRM_Export_{date.today().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# KPI METRIC CARDS
# ==========================================
total_leads = len(st.session_state.leads_data)
total_pipeline_val = st.session_state.leads_data["Deal_Value_INR"].sum()
won_df = st.session_state.leads_data[st.session_state.leads_data["Pipeline_Stage"] == "Deal Won"]
won_revenue = won_df["Deal_Value_INR"].sum()
conversion_rate = (len(won_df) / total_leads * 100) if total_leads > 0 else 0
avg_deal_size = (total_pipeline_val / total_leads) if total_leads > 0 else 0

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Inbound Leads", f"{total_leads} leads")
m2.metric("Total Pipeline Value", f"₹{total_pipeline_val:,.0f}")
m3.metric("Closed Won Revenue", f"₹{won_revenue:,.0f}")
m4.metric("Conversion Rate", f"{conversion_rate:.1f}%")
m5.metric("Avg Deal Size", f"₹{avg_deal_size:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# APPLICATION TABS
# ==========================================
tab_analytics, tab_pipeline, tab_add, tab_import = st.tabs([
    "📊 Pipeline Analytics",
    "📋 Lead Manager & Actions",
    "➕ Add New Lead",
    "📁 Import External CSV/Excel",
])

# ------------------------------------------
# TAB 1: PIPELINE ANALYTICS
# ------------------------------------------
with tab_analytics:
    st.subheader("Visual Sales Pipeline Performance")

    c1, c2 = st.columns(2)

    with c1:
        # Leads by Pipeline Stage
        stage_order = ["New Lead", "Contacted", "Proposal Sent", "Deal Won", "Lost"]
        stage_counts = st.session_state.leads_data["Pipeline_Stage"].value_counts().reindex(stage_order).fillna(0).reset_index()
        stage_counts.columns = ["Stage", "Count"]

        stage_colors = {
            "New Lead": "#6366f1",
            "Contacted": "#f59e0b",
            "Proposal Sent": "#0284c7",
            "Deal Won": "#10b981",
            "Lost": "#ef4444",
        }

        fig_stage = px.bar(
            stage_counts,
            x="Stage",
            y="Count",
            color="Stage",
            color_discrete_map=stage_colors,
            text="Count",
            title="Leads Distribution by Pipeline Stage",
        )
        fig_stage.update_layout(showlegend=False, height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_stage, use_container_width=True)

    with c2:
        # Revenue by Service Required
        service_rev = (
            st.session_state.leads_data.groupby("Service_Required")["Deal_Value_INR"]
            .sum()
            .reset_index()
            .sort_values(by="Deal_Value_INR", ascending=False)
        )
        fig_service = px.pie(
            service_rev,
            names="Service_Required",
            values="Deal_Value_INR",
            hole=0.45,
            title="Pipeline Value Breakdown by Service (₹)",
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
        fig_service.update_traces(textposition="inside", textinfo="percent+label")
        fig_service.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_service, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        # Lead Source Effectiveness
        source_df = (
            st.session_state.leads_data.groupby(["Lead_Source", "Pipeline_Stage"])
            .size()
            .reset_index(name="Count")
        )
        fig_source = px.bar(
            source_df,
            x="Lead_Source",
            y="Count",
            color="Pipeline_Stage",
            color_discrete_map=stage_colors,
            title="Lead Volume & Quality by Acquisition Channel",
            barmode="stack",
        )
        fig_source.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_source, use_container_width=True)

    with c4:
        # High-Priority Pipeline Value by Client
        top_leads = (
            st.session_state.leads_data.sort_values(by="Deal_Value_INR", ascending=False)
            .head(7)
            .copy()
        )
        fig_top = px.bar(
            top_leads,
            x="Deal_Value_INR",
            y="Company",
            orientation="h",
            color="Pipeline_Stage",
            color_discrete_map=stage_colors,
            title="Top 7 Highest Value Opportunities (₹)",
            text="Deal_Value_INR",
        )
        fig_top.update_layout(
            yaxis=dict(autorange="reversed"),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_top, use_container_width=True)

# ------------------------------------------
# TAB 2: LEAD MANAGER & DIRECT ACTIONS
# ------------------------------------------
with tab_pipeline:
    st.subheader(f"Lead Pipeline Records ({len(filtered_df)} shown)")

    if len(filtered_df) == 0:
        st.info("No leads match the selected filters. Adjust sidebar filters to view records.")
    else:
        # Display styled table
        display_df = filtered_df.copy()
        display_df["Deal_Value"] = display_df["Deal_Value_INR"].apply(lambda v: f"₹{v:,.0f}")
        
        # Streamlit interactive dataframe
        st.dataframe(
            display_df[[
                "Lead_ID", "Client_Name", "Company", "Deal_Value", 
                "Pipeline_Stage", "Priority", "Service_Required", 
                "Lead_Source", "Next_Follow_Up", "Notes"
            ]],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("---")
        st.markdown("#### ⚡ 1-Click Direct Outreach & Action Hub")
        st.caption("Select any client from the list below to initiate direct WhatsApp conversation or update deal status:")

        lead_options = {
            f"{r['Lead_ID']} — {r['Client_Name']} ({r['Company']})": r["Lead_ID"]
            for _, r in filtered_df.iterrows()
        }

        if lead_options:
            selected_label = st.selectbox("Choose Prospect:", list(lead_options.keys()))
            selected_id = lead_options[selected_label]
            selected_row = filtered_df[filtered_df["Lead_ID"] == selected_id].iloc[0]

            with st.container():
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; margin-top: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <div>
                                <h4 style="margin: 0; color: #0F172A; font-size: 1.15rem;">{selected_row['Client_Name']} — <span style="color: #64748B;">{selected_row['Company']}</span></h4>
                                <div style="font-size: 0.85rem; color: #64748B; margin-top: 3px;">Service: <strong>{selected_row['Service_Required']}</strong> | Source: <strong>{selected_row['Lead_Source']}</strong></div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.25rem; font-weight: 800; color: #10B981;">₹{selected_row['Deal_Value_INR']:,.0f}</div>
                                <div style="font-size: 0.8rem; font-weight: 700; color: #2563EB;">{selected_row['Pipeline_Stage']} ({selected_row['Priority']} Priority)</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c_act1, c_act2 = st.columns([1.5, 2.5])
                with c_act1:
                    wa_message = f"Hi {selected_row['Client_Name']}, this is Onkar Hande. Following up regarding your inquiry for {selected_row['Service_Required']} at {selected_row['Company']}."
                    wa_url = f"https://wa.me/{selected_row['Phone']}?text={wa_message.replace(' ', '%20')}"

                    st.markdown(
                        f"""
                        <div style="margin-top: 15px;">
                            <a href="{wa_url}" target="_blank" class="wa-btn" style="padding: 10px 20px; font-size: 0.95rem; display: inline-block;">
                                💬 WhatsApp {selected_row['Client_Name'].split()[0]} Directly
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.caption(f"Phone: +{selected_row['Phone']} • Email: [{selected_row['Email']}](mailto:{selected_row['Email']})")

                with c_act2:
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    new_stage_select = st.selectbox(
                        "Update Pipeline Stage:",
                        ["New Lead", "Contacted", "Proposal Sent", "Deal Won", "Lost"],
                        index=["New Lead", "Contacted", "Proposal Sent", "Deal Won", "Lost"].index(selected_row["Pipeline_Stage"]),
                        key=f"stage_updater_{selected_id}",
                    )
                    if st.button("💾 Update Deal Stage", key=f"btn_update_{selected_id}"):
                        st.session_state.leads_data.loc[
                            st.session_state.leads_data["Lead_ID"] == selected_id, "Pipeline_Stage"
                        ] = new_stage_select
                        st.success(f"Updated {selected_row['Client_Name']} to '{new_stage_select}'!")
                        st.rerun()

                st.info(f"📝 **Internal Notes & Scope:** {selected_row['Notes']} (Scheduled Follow-up: {selected_row['Next_Follow_Up']})")

# ------------------------------------------
# TAB 3: ADD NEW LEAD
# ------------------------------------------
with tab_add:
    st.subheader("➕ Register New Inbound Opportunity")
    st.markdown("Quickly capture prospects from incoming calls, WhatsApp inquiries, or website forms.")

    with st.form("new_lead_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            name_input = st.text_input("Client Full Name *", placeholder="e.g. Ramesh Kadam")
            company_input = st.text_input("Company / Business Name *", placeholder="e.g. Kadam Supermarket Pune")
            phone_input = st.text_input("WhatsApp / Phone (with country code, e.g. 919876543210) *")
            email_input = st.text_input("Email Address", placeholder="e.g. ramesh@kadammart.com")
            source_input = st.selectbox("Lead Source", ["Website", "LinkedIn", "Google Ads", "Instagram", "Referral", "Cold Outreach"])

        with f_col2:
            service_input = st.selectbox("Service Required", [
                "Excel Automation & Cleaning",
                "n8n Workflow Automation",
                "E-Commerce Development",
                "Power BI Dashboard",
                "Lead Generation",
                "Custom Python Tooling"
            ])
            deal_val_input = st.number_input("Estimated Deal Value (₹) *", min_value=1000, value=25000, step=1000)
            stage_input = st.selectbox("Initial Pipeline Stage", ["New Lead", "Contacted", "Proposal Sent", "Deal Won", "Lost"])
            priority_input = st.selectbox("Priority Level", ["High", "Medium", "Low"])
            follow_up_input = st.date_input("Scheduled Next Follow-Up", value=date.today())
            notes_input = st.text_area("Client Notes / Requirements Summary", placeholder="Specific project scope, timeline, or pain points...")

        submitted = st.form_submit_button("💼 Save Lead to CRM Pipeline", use_container_width=True)

        if submitted:
            if not name_input or not company_input:
                st.error("Please provide both Client Name and Company Name.")
            else:
                # Generate unique ID
                current_count = len(st.session_state.leads_data) + 101
                new_id = f"LEAD-{current_count}"
                clean_phone = "".join(filter(str.isdigit, phone_input)) or "919999999999"

                new_row = {
                    "Lead_ID": new_id,
                    "Client_Name": name_input.strip(),
                    "Company": company_input.strip(),
                    "Phone": clean_phone,
                    "Email": email_input.strip() or "client@example.com",
                    "Lead_Source": source_input,
                    "Service_Required": service_input,
                    "Deal_Value_INR": deal_val_input,
                    "Pipeline_Stage": stage_input,
                    "Priority": priority_input,
                    "Next_Follow_Up": follow_up_input.strftime("%Y-%m-%d"),
                    "Notes": notes_input.strip() or "New prospect created.",
                }

                # Append to session state
                st.session_state.leads_data = pd.concat(
                    [st.session_state.leads_data, pd.DataFrame([new_row])],
                    ignore_index=True,
                )
                st.success(f"✅ Lead {new_id} ({name_input}) successfully added to CRM!")
                st.rerun()

# ------------------------------------------
# TAB 4: IMPORT EXTERNAL FILE
# ------------------------------------------
with tab_import:
    st.subheader("📁 Import Your Own Leads Dataset")
    st.markdown("Upload any existing CSV or Excel spreadsheet to analyze your sales pipeline inside LeadFlow.")

    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                imported_df = pd.read_csv(uploaded_file)
            else:
                imported_df = pd.read_excel(uploaded_file)

            st.write(f"**Preview of Uploaded Data ({len(imported_df)} rows):**")
            st.dataframe(imported_df.head(5), use_container_width=True)

            if st.button("📥 Load Uploaded Data into Dashboard", use_container_width=True):
                # Basic normalization of expected columns
                if "Deal_Value_INR" not in imported_df.columns:
                    for col in imported_df.columns:
                        if "deal" in col.lower() or "amount" in col.lower() or "value" in col.lower():
                            imported_df.rename(columns={col: "Deal_Value_INR"}, inplace=True)
                            break
                    if "Deal_Value_INR" not in imported_df.columns:
                        imported_df["Deal_Value_INR"] = 25000

                if "Pipeline_Stage" not in imported_df.columns:
                    imported_df["Pipeline_Stage"] = "New Lead"
                if "Priority" not in imported_df.columns:
                    imported_df["Priority"] = "Medium"
                if "Lead_Source" not in imported_df.columns:
                    imported_df["Lead_Source"] = "Website"
                if "Company" not in imported_df.columns:
                    imported_df["Company"] = "Enterprise Client"
                if "Client_Name" not in imported_df.columns:
                    imported_df["Client_Name"] = "Prospective Lead"
                if "Phone" not in imported_df.columns:
                    imported_df["Phone"] = "919999999999"
                if "Email" not in imported_df.columns:
                    imported_df["Email"] = "prospect@example.com"
                if "Lead_ID" not in imported_df.columns:
                    imported_df["Lead_ID"] = [f"LEAD-{i+101}" for i in range(len(imported_df))]
                if "Next_Follow_Up" not in imported_df.columns:
                    imported_df["Next_Follow_Up"] = date.today().strftime("%Y-%m-%d")
                if "Notes" not in imported_df.columns:
                    imported_df["Notes"] = "Imported external record."

                st.session_state.leads_data = imported_df
                st.success(f"Successfully loaded {len(imported_df)} leads into LeadFlow CRM!")
                st.rerun()

        except Exception as e:
            st.error(f"Error parsing uploaded file: {str(e)}")

# ==========================================
# FOOTER
# ==========================================
st.markdown(
    """
    <div class="crm-footer">
        <strong>LeadFlow CRM Suite &copy; 2026</strong> • Enterprise Sales Intelligence & Pipeline Automation<br>
        Engineered with Python, Streamlit &amp; Plotly by <strong>Onkar Hande</strong> (BCA / MCA)<br>
        <a href="https://onkarhande96.github.io" target="_blank">View Live Portfolio</a> • 
        <a href="https://github.com/Onkarhande96" target="_blank">GitHub Profile</a> • 
        <a href="https://linkedin.com/in/onkarhande96" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)
