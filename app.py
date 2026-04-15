import streamlit as st
from main import process_partners, create_gmail_draft

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Automated Email Assistant")

st.title("📧 Automated Email Assistant")
st.caption("Generate personalized follow-up emails for mill partners based on compliance data.")
# ---------------- FLAG FUNCTION ----------------
def get_flag(rate):
    if rate >= 90:
        return "🟢 High Performer"
    elif rate >= 80:
        return "🟡 Moderate"
    else:
        return "🔴 Needs Attention"

# ---------------- INPUT ----------------
sheet_name = st.text_input(
    "Enter Google Sheet Name",
    "Mill Partner Compliance"
)

# ---------------- GENERATE ----------------
if st.button("🚀 Generate Emails"):
    with st.spinner("Generating emails using AI..."):
        results, creds = process_partners(sheet_name)

        # Sort by compliance (lowest first)
        results.sort(key=lambda x: x["rate"])

        st.session_state["emails"] = results
        st.session_state["creds"] = creds

# ---------------- DISPLAY ----------------
if "emails" in st.session_state:

    emails = st.session_state["emails"]

    # -------- DASHBOARD --------
    st.subheader("📊 Summary")

    total = len(emails)
    high = sum(1 for e in emails if e["rate"] >= 90)
    low = sum(1 for e in emails if e["rate"] < 80)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("High Performers", high)
    col3.metric("Needs Attention", low)

    st.success(f"{total} personalized emails generated successfully!")

    # -------- EMAIL SECTION --------
    st.subheader("📬 Partner Emails")

    for i, email in enumerate(emails):

        flag = get_flag(email["rate"])

        # Clean row layout
        col1, col2 = st.columns([5, 1])
        col1.write(f"{flag} {email['name']}")
        col2.markdown(f"**{int(email['rate'])}%**")

        # Expandable email view
        with st.expander(f"View Email → {email['email']}"):

            subject = st.text_input(
                "Subject",
                email["subject"],
                key=f"sub_{i}"
            )

            body = st.text_area(
                "Body",
                email["body"],
                height=200,
                key=f"body_{i}"
            )

            if st.button("✉️ Create Draft", key=f"draft_{i}"):
                create_gmail_draft(
                    st.session_state["creds"],
                    email["email"],
                    subject,
                    body
                )
                st.success("Draft created!")

    # -------- BULK ACTION --------
    st.divider()

    if st.button("📨 Create ALL Drafts"):
        for i, email in enumerate(emails):
            create_gmail_draft(
                st.session_state["creds"],
                email["email"],
                st.session_state[f"sub_{i}"],
                st.session_state[f"body_{i}"]
            )

        st.success("All drafts created successfully!")
