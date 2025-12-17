import streamlit as st
import qrcode
import uuid
import os
import sqlite3
from datetime import datetime
from PIL import Image

from utils import STATIONS, calculate_distance, calculate_fare, calculate_co2
from database import create_tables, save_booking, save_ticket

# ---------------- BASIC SETUP ----------------
st.set_page_config(
    page_title="Hyderabad Metro Smart Ticket",
    layout="centered"
)

create_tables()

if not os.path.exists("tickets"):
    os.makedirs("tickets")

# Session state
if "paid" not in st.session_state:
    st.session_state.paid = False
if "txn_id" not in st.session_state:
    st.session_state.txn_id = None
if "show_payment" not in st.session_state:
    st.session_state.show_payment = False

# ---------------- UI HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>🚇 Hyderabad Metro Smart Ticket</h1>",
    unsafe_allow_html=True
)
st.caption("QR Ticketing | Fake Payment Gateway | SQLite Database | Eco Friendly")
st.markdown("---")

# ---------------- USER INPUT ----------------
ticket_for = st.selectbox("🎟 Ticket For", ["Myself", "Others"])
if ticket_for == "Others":
    contact = st.text_input("📲 Receiver Email / Phone")

col1, col2 = st.columns(2)
with col1:
    from_station = st.selectbox("🚉 From", STATIONS)
with col2:
    to_station = st.selectbox("🚉 To", STATIONS)

tickets_count = st.number_input(
    "🎫 Number of Tickets",
    min_value=1,
    max_value=10,
    value=1
)

journey_date = st.date_input("📅 Journey Date")

# ---------------- CALCULATIONS ----------------
fare = 0
co2 = 0

if from_station != to_station:
    distance = calculate_distance(from_station, to_station)
    fare = calculate_fare(distance, tickets_count)
    co2 = calculate_co2(distance, tickets_count)

    st.info(
        f"📏 Distance: {distance:.1f} km   |   💰 Total Fare: ₹{fare}"
    )
else:
    st.warning("From and To stations must be different")

# ---------------- PAYMENT ----------------
if st.button("💳 Proceed to Payment"):
    if from_station == to_station:
        st.error("Invalid journey selection")
    else:
        st.session_state.show_payment = True

if st.session_state.show_payment and not st.session_state.paid:
    st.subheader("💳 Fake Payment Gateway")
    st.radio("Select Payment Method", ["UPI", "Debit Card", "Net Banking"])
    st.warning(f"Payable Amount: ₹{fare}")

    if st.button("✅ Confirm Payment"):
        st.session_state.paid = True
        st.session_state.txn_id = "TXN" + str(uuid.uuid4())[:10].upper()

        created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

        save_booking(
            st.session_state.txn_id,
            from_station,
            to_station,
            tickets_count,
            fare,
            journey_date.strftime("%d-%m-%Y"),
            created_at
        )

        st.success("🎉 Payment Successful")

# ---------------- TICKET GENERATION ----------------
if st.session_state.paid:
    st.markdown("---")
    st.success(f"Transaction ID: {st.session_state.txn_id}")
    st.subheader("🎫 Your Metro Tickets")

    for i in range(1, tickets_count + 1):
        ticket_id = str(uuid.uuid4())[:8]
        save_ticket(st.session_state.txn_id, ticket_id)

        qr_data = f"""
Hyderabad Metro Smart Ticket
Ticket {i} of {tickets_count}
Ticket ID: {ticket_id}
From: {from_station}
To: {to_station}
Journey Date: {journey_date}
Transaction ID: {st.session_state.txn_id}
"""

        qr_img = qrcode.make(qr_data)
        file_path = f"tickets/{ticket_id}.png"
        qr_img.save(file_path)

        st.image(
            Image.open(file_path),
            caption=f"🎟 Ticket {i}",
            use_column_width=False
        )

        with open(file_path, "rb") as f:
            st.download_button(
                f"⬇ Download Ticket {i}",
                data=f,
                file_name=f"metro_ticket_{ticket_id}.png",
                mime="image/png",
                key=ticket_id
            )

    st.info(f"🌱 You saved **{co2} kg CO₂** by choosing Metro 🚆")

    if ticket_for == "Others":
        st.success(f"📩 Ticket details can be shared with: {contact}")

# ---------------- ADMIN DATABASE VIEW (CLOUD SAFE) ----------------
st.markdown("---")
if st.checkbox("🔐 Admin: View Stored Database Data"):
    conn = sqlite3.connect("metro.db", check_same_thread=False)
    cur = conn.cursor()

    st.subheader("📄 Bookings Table")
    bookings = cur.execute("SELECT * FROM bookings").fetchall()
    st.write(bookings)

    st.subheader("🎫 Ticket Details Table")
    tickets = cur.execute("SELECT * FROM ticket_details").fetchall()
    st.write(tickets)

    conn.close()
