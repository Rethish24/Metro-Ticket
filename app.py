from database import create_tables, save_booking, save_ticket
import streamlit as st
import qrcode
import uuid
import os
from datetime import datetime
from PIL import Image
from utils import STATIONS, calculate_distance, calculate_fare, calculate_co2

# ---------------- SETUP ----------------
st.set_page_config(page_title="Hyderabad Metro Smart Ticket", layout="centered")

if not os.path.exists("tickets"):
    os.makedirs("tickets")

# Session states
if "paid" not in st.session_state:
    st.session_state.paid = False
if "txn_id" not in st.session_state:
    st.session_state.txn_id = None
if "show_payment" not in st.session_state:
    st.session_state.show_payment = False

# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center;'>🚇 Hyderabad Metro Smart Ticket</h1>", unsafe_allow_html=True)
st.caption("🔐 Payment Gateway: Demo / Simulation Mode")
st.markdown("---")

ticket_for = st.selectbox("🎟 Ticket For", ["Myself", "Others"])
if ticket_for == "Others":
    contact = st.text_input("📲 Receiver Email / Phone")

col1, col2 = st.columns(2)
with col1:
    from_station = st.selectbox("🚉 From", STATIONS)
with col2:
    to_station = st.selectbox("🚉 To", STATIONS)

tickets_count = st.number_input("🎫 Number of Tickets", min_value=1, max_value=10, value=1)
journey_date = st.date_input("📅 Journey Date")

# ---------------- FARE CALC ----------------
if from_station != to_station:
    distance = calculate_distance(from_station, to_station)
    fare = calculate_fare(distance, tickets_count)
    co2 = calculate_co2(distance, tickets_count)

    st.info(f"📏 Distance: {distance:.1f} km | 💰 Total Fare: ₹{fare}")
else:
    fare = 0

# ---------------- PAYMENT ----------------
if st.button("💳 Proceed to Payment"):
    if from_station == to_station:
        st.error("From and To stations cannot be the same")
    else:
        st.session_state.show_payment = True

if st.session_state.show_payment and not st.session_state.paid:
    st.markdown("## 💳 Secure Payment Gateway")

    st.radio("Select Payment Method", ["UPI", "Debit Card", "Credit Card", "Net Banking"])
    st.warning(f"Amount to Pay: ₹{fare}")

    if st.button("✅ Confirm Payment"):
        st.session_state.paid = True
        st.session_state.txn_id = "TXN" + str(uuid.uuid4())[:10].upper()
        st.success("🎉 Payment Successful")

# ---------------- TICKET GENERATION ----------------
if st.session_state.paid:
    st.markdown("---")
    st.success(f"Transaction ID: {st.session_state.txn_id}")

    time_now = datetime.now().strftime("%d-%m-%Y %H:%M")

    st.markdown("## 🎫 Your Metro Tickets")

    for i in range(1, tickets_count + 1):
        ticket_id = str(uuid.uuid4())[:8]

        qr_data = f"""
        Hyderabad Metro Ticket
        Ticket No: {i} of {tickets_count}
        Ticket ID: {ticket_id}
        From: {from_station}
        To: {to_station}
        Fare: ₹{fare // tickets_count}
        Date: {journey_date}
        TXN: {st.session_state.txn_id}
        Issued: {time_now}
        """

        qr = qrcode.make(qr_data)
        file_path = f"tickets/{ticket_id}.png"
        qr.save(file_path)

        st.image(Image.open(file_path), caption=f"🎟 Ticket {i}")

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
        st.warning(f"📩 Tickets can be shared with: {contact}")

