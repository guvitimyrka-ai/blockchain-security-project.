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
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, ["Генезис-блок"], time(), "0")
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        new_block = Block(len(self.chain), transactions, time(), self.chain[-1].hash)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash != self.chain[i].compute_hash(): return False, i
            if self.chain[i].previous_hash != self.chain[i-1].hash: return False, i
        return True, None

# 2. Настройка интерфейса
st.set_page_config(page_title="CryptoGuard Ledger", layout="wide")

# Инициализация (самый важный момент!)
if 'bc' not in st.session_state:
    st.session_state.bc = Blockchain()

st.title("🛡️ CryptoGuard Ledger")
st.write("Коммерческая система мониторинга целостности блокчейн-узла")

# Основной контент
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Управление блоками")
    data = st.text_input("Введите данные транзакции:", placeholder="Напр: 'Оплата счета №104'")
    if st.button("Добавить блок в цепь"):
        if data:
            st.session_state.bc.add_block([data])
            st.rerun()

    st.divider()
    st.subheader("Симуляция атаки")
    if len(st.session_state.bc.chain) > 1:
        if st.button("🚨 Взломать блок №1"):
            st.session_state.bc.chain[1].transactions = ["⚠️ ДАННЫЕ ПОДМЕНЕНЫ!"]
            st.rerun()
    else:
        st.info("Добавьте хотя бы один блок для теста атак.")

with col2:
    valid, err_idx = st.session_state.bc.is_valid()
    if valid:
        st.success("✅ Статус: VALID (Данные защищены)")
    else:
        st.error(f"❌ Статус: INVALID (Взлом в блоке №{err_idx}!)")

    for b in reversed(st.session_state.bc.chain):
        with st.expander(f"📦 Блок №{b.index} | Хеш: {b.hash[:10]}..."):
            st.write(f"**Данные:** {b.transactions}")
            st.write(f"**Хеш:** {b.hash}")
            st.write(f"**Пред. хеш:** {b.previous_hash}")with col1:
    st.subheader("Управление блоками")
    data = st.text_input("Введите данные транзакции:", placeholder="Напр: 'Оплата счета №104'")
    
    # Кнопки в одну строку для красоты
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("Добавить блок"):
            if data:
                st.session_state.bc.add_block([data])
                st.rerun()
    
    with btn_col2:
        if st.button("🗑️ Сбросить всё"):
            # Полная очистка состояния
            del st.session_state.bc
            st.rerun()

    st.divider()
    # ... далее остальной код про взлом ...
