import streamlit as st
import hashlib
import json
from time import time

# 1. Логика Блокчейна
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        # Используем строго определенный порядок ключей для стабильного хеша
        block_data = {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Фиксируем время для генезиса
        genesis_block = Block(0, ["Генезис-блок"], 1713250000.0, "0")
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        new_block = Block(len(self.chain), transactions, time(), self.chain[-1].hash)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            # Проверка текущего хеша
            if current.hash != current.compute_hash():
                return False, i
            # Проверка связи с предыдущим
            if current.previous_hash != previous.hash:
                return False, i
        return True, None

# 2. Интерфейс
st.set_page_config(page_title="CryptoGuard Ledger", layout="wide")

if 'bc' not in st.session_state:
    st.session_state.bc = Blockchain()

st.title("🛡️ CryptoGuard Ledger")
st.write("Система мониторинга целостности блокчейн-узла")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Управление")
    data = st.text_input("Данные транзакции:", placeholder="Напр: 'Счет №104'")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ Добавить"):
            if data:
                st.session_state.bc.add_block([data])
                st.rerun()
    with c2:
        if st.button("🗑️ Сброс"):
            st.session_state.bc = Blockchain()
            st.rerun()

    st.divider()
    st.subheader("Тест атаки")
    if len(st.session_state.bc.chain) > 1:
        if st.button("🚨 Взломать блок №1"):
            st.session_state.bc.chain[1].transactions = ["⚠️ ПОДМЕНА!"]
            st.rerun()
    else:
        st.info("Добавьте блок для теста.")

with col2:
    valid, err_idx = st.session_state.bc.is_valid()
    if valid:
        st.success("✅ Статус: VALID")
    else:
        st.error(f"❌ Статус: INVALID (Блок №{err_idx})")

    for b in reversed(st.session_state.bc.chain):
        with st.expander(f"📦 Блок №{b.index}"):
            st.json({"Хеш": b.hash, "Пред. хеш": b.previous_hash, "Данные": b.transactions})
