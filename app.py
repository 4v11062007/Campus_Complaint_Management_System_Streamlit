import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Campus Complaint Management System",
    page_icon="🏫",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "complaints" not in st.session_state:
    st.session_state.complaints = []

if "complaint_counter" not in st.session_state:
    st.session_state.complaint_counter = 1001

if "notifications" not in st.session_state:
    st.session_state.notifications = []

def generate_complaint_id():
    complaint_id = f"CMP{st.session_state.complaint_counter}"
    st.session_state.complaint_counter += 1
    return complaint_id

def logout():
    st.session_state.logged_in = False
    st.rerun()

if not st.session_state.logged_in:

    st.title("🏫 Campus Complaint Management System")
    st.subheader("Student Complaint Registration Portal")

    st.write(
        "A centralized platform for registering, tracking and managing "
        "campus-related complaints."
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.header("🔐 Login")

        role = st.selectbox(
            "Select Role",
            ["Student", "Administrator"]
        )

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button("Login", use_container_width=True):

            if username.strip() == "" or password.strip() == "":
                st.warning("⚠️ Please enter both username and password.")

            elif role == "Student" and username == "student" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.role = "Student"
                st.session_state.username = username
                st.success("✅ Student login successful!")
                st.rerun()

            elif role == "Administrator" and username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "Administrator"
                st.session_state.username = username
                st.success("✅ Administrator login successful!")
                st.rerun()

            else:
                st.error("❌ Invalid username, password or role.")

else:

    st.sidebar.title("🏫 Campus CMS")

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    st.sidebar.write(
        f"Role: **{st.session_state.role}**"
    )

    menu_options = [
        "🏠 Dashboard",
        "📝 Register Complaint",
        "🔎 Search Complaints",
        "📋 All Complaints",
        "📢 Notifications"
    ]

    selected_menu = st.sidebar.radio(
        "Navigation",
        menu_options
    )

    st.sidebar.divider()

    if st.sidebar.button("🔄 Refresh Page", use_container_width=True):
        st.rerun()

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()

    st.title("🏫 Campus Complaint Management System")

    st.caption(
        f"Welcome, {st.session_state.username} | "
        f"{st.session_state.role}"
    )

    st.divider()

    if selected_menu == "🏠 Dashboard":

        st.header("📊 Complaint Dashboard")

        total_complaints = len(st.session_state.complaints)

        pending = len([
            c for c in st.session_state.complaints
            if c["Status"] == "Pending"
        ])

        resolved = len([
            c for c in st.session_state.complaints
            if c["Status"] == "Resolved"
        ])

        high_priority = len([
            c for c in st.session_state.complaints
            if c["Priority"] == "High"
        ])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Complaints",
                total_complaints
            )

        with col2:
            st.metric(
                "Pending",
                pending
            )

        with col3:
            st.metric(
                "Resolved",
                resolved
            )

        with col4:
            st.metric(
                "High Priority",
                high_priority
            )

        st.divider()

        st.subheader("📌 System Information")

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                "Students can register complaints related to "
                "academics, infrastructure, hostel, IT and other "
                "campus services."
            )

        with col2:
            st.success(
                "Administrators can monitor complaints and "
                "track their current status."
            )

        st.divider()

        if st.button("📖 View Complaint Guidelines"):

            st.info(
                "Please provide clear and accurate information "
                "while registering a complaint. Avoid submitting "
                "duplicate or inappropriate complaints."
            )

    elif selected_menu == "📝 Register Complaint":

        st.header("📝 Register a New Complaint")

        with st.form("complaint_form"):

            col1, col2 = st.columns(2)

            with col1:

                student_name = st.text_input(
                    "Student Name"
                )

                student_id = st.text_input(
                    "Student ID"
                )

                category = st.selectbox(
                    "Complaint Category",
                    [
                        "Academic",
                        "Hostel",
                        "Infrastructure",
                        "IT Support",
                        "Library",
                        "Transport",
                        "Cafeteria",
                        "Other"
                    ]
                )

            with col2:

                priority = st.selectbox(
                    "Priority",
                    [
                        "Low",
                        "Medium",
                        "High",
                        "Critical"
                    ]
                )

                location = st.text_input(
                    "Location",
                    placeholder="Example: Block 2, Room 705"
                )

                complaint_title = st.text_input(
                    "Complaint Title"
                )

            description = st.text_area(
                "Complaint Description",
                placeholder="Describe your complaint in detail..."
            )

            submitted = st.form_submit_button(
                "🚀 Submit Complaint",
                use_container_width=True
            )

            if submitted:

                if (
                    student_name.strip() == ""
                    or student_id.strip() == ""
                    or location.strip() == ""
                    or complaint_title.strip() == ""
                    or description.strip() == ""
                ):

                    st.error(
                        "❌ Please fill in all required fields."
                    )

                elif len(description.strip()) < 10:

                    st.warning(
                        "⚠️ Complaint description should contain "
                        "at least 10 characters."
                    )

                else:

                    complaint_id = generate_complaint_id()

                    complaint = {
                        "Complaint ID": complaint_id,
                        "Student Name": student_name,
                        "Student ID": student_id,
                        "Category": category,
                        "Priority": priority,
                        "Location": location,
                        "Title": complaint_title,
                        "Description": description,
                        "Status": "Pending",
                        "Date": datetime.now().strftime(
                            "%d-%m-%Y %H:%M"
                        )
                    }

                    st.session_state.complaints.append(
                        complaint
                    )

                    st.session_state.notifications.append(
                        f"Complaint {complaint_id} was registered successfully."
                    )

                    st.success(
                        f"✅ Complaint submitted successfully!\n\n"
                        f"Your Complaint ID is **{complaint_id}**"
                    )

                    st.balloons()

    elif selected_menu == "🔎 Search Complaints":

        st.header("🔎 Search Complaints")

        search_term = st.text_input(
            "Enter Complaint ID or Student ID",
            placeholder="Example: CMP1001"
        )

        if search_term:

            results = [
                complaint
                for complaint in st.session_state.complaints
                if search_term.lower() in complaint["Complaint ID"].lower()
                or search_term.lower() in complaint["Student ID"].lower()
            ]

            if results:

                st.success(
                    f"{len(results)} complaint(s) found."
                )

                for complaint in results:

                    with st.expander(
                        f"{complaint['Complaint ID']} - "
                        f"{complaint['Title']}"
                    ):

                        st.write(
                            f"**Student:** {complaint['Student Name']}"
                        )

                        st.write(
                            f"**Category:** {complaint['Category']}"
                        )

                        st.write(
                            f"**Priority:** {complaint['Priority']}"
                        )

                        st.write(
                            f"**Location:** {complaint['Location']}"
                        )

                        st.write(
                            f"**Status:** {complaint['Status']}"
                        )

                        st.write(
                            f"**Date:** {complaint['Date']}"
                        )

                        st.write(
                            f"**Description:** "
                            f"{complaint['Description']}"
                        )

            else:

                st.warning(
                    "No complaints found."
                )

    elif selected_menu == "📋 All Complaints":

        st.header("📋 Complaint Records")

        if len(st.session_state.complaints) == 0:

            st.info(
                "No complaints have been registered yet."
            )

        else:

            display_data = [
                {
                    "Complaint ID": c["Complaint ID"],
                    "Student ID": c["Student ID"],
                    "Category": c["Category"],
                    "Priority": c["Priority"],
                    "Location": c["Location"],
                    "Status": c["Status"],
                    "Date": c["Date"]
                }
                for c in st.session_state.complaints
            ]

            st.dataframe(
                display_data,
                use_container_width=True
            )

            if st.session_state.role == "Administrator":

                st.divider()

                st.subheader(
                    "⚙️ Administrator Controls"
                )

                complaint_ids = [
                    c["Complaint ID"]
                    for c in st.session_state.complaints
                ]

                selected_id = st.selectbox(
                    "Select Complaint",
                    complaint_ids
                )

                new_status = st.selectbox(
                    "Update Status",
                    [
                        "Pending",
                        "In Progress",
                        "Resolved",
                        "Rejected"
                    ]
                )

                if st.button("Update Complaint Status"):

                    for complaint in st.session_state.complaints:

                        if complaint["Complaint ID"] == selected_id:

                            complaint["Status"] = new_status

                            st.session_state.notifications.append(
                                f"Complaint {selected_id} status changed to {new_status}."
                            )

                            st.success(
                                f"Complaint {selected_id} updated successfully."
                            )

                            st.rerun()

    elif selected_menu == "📢 Notifications":

        st.header("📢 Notifications & Alerts")

        if len(st.session_state.notifications) == 0:

            st.info(
                "No new notifications."
            )

        else:

            for notification in reversed(
                st.session_state.notifications
            ):

                st.success(
                    f"🔔 {notification}"
                )

    st.divider()

    st.caption(
        "Campus Complaint Management System | "
        "Developed using Streamlit"
    )
