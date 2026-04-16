import streamlit as st
import hashlib
import json
from time import time

# --- ЛОГИКА ИЗ ВАШЕГО ПРИЛОЖЕНИЯ 2 ---
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0")
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.compute_hash():
                return False, i
            if current.previous_hash != previous.hash:
                return False, i
        return True, None

# --- GUI ИНТЕРФЕЙС (STREAMLIT) ---
st.set_page_config(page_title="CryptoGuard Ledger v1.0", layout="wide")

st.title("🛡️ CryptoGuard Ledger")
st.subheader("Коммерческая система мониторинга целостности блокчейн-узла")

# Инициализация блокчейна в сессии
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Боковая панель (Sidebar) с информацией из Приложения 1
st.sidebar.header("Спецификации системы")
st.sidebar.info("""
**Используемые алгоритмы:**
- **Хеширование:** SHA-256 (256 бит)
- **Целостность:** Проверка связей блоков
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.write("### Управление блоками")
    data = st.text_input("Введите данные транзакции:", placeholder="Напр: 'Оплата счета №104'")
    
    if st.button("Добавить блок в цепь"):
        last_block = st.session_state.blockchain.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=[data],
            timestamp=time(),
            previous_hash=last_block.hash
        )
        st.session_state.blockchain.add_block(new_block)
        st.success(f"Блок #{new_block.index} успешно добавлен!")

    st.divider()
    
 # Находим этот раздел в коде и заменяем его:
st.subheader("Симуляция атаки (Тестирование)")


if len(st.session_state.bc.chain) > 1:
    block_to_hack = st.number_input("Номер блока для взлома:", min_value=1, max_value=len(st.session_state.bc.chain)-1, step=1)
    if st.button("🚨 Взломать выбранный блок"):
        st.session_state.bc.chain[block_to_hack].transactions = ["⚠️ ДАННЫЕ ПОДМЕНЕНЫ!"]
        st.rerun()
else:
    st.info("Добавьте хотя бы один блок (кроме Генезиса), чтобы разблокировать систему тестирования атак.")
if len(st.session_state.bc.chain) > 1:
    block_to_hack = st.number_input("Номер блока для взлома:", min_value=1, max_value=len(st.session_state.bc.chain)-1, step=1)
    if st.button("🚨 Взломать выбранный блок"):
        st.session_state.bc.chain[block_to_hack].transactions = ["⚠️ ДАННЫЕ ПОДМЕНЕНЫ!"]
        st.rerun()
else:
    st.info("Добавьте хотя бы один блок (кроме Генезиса), чтобы разблокировать систему тестирования атак.")

if len(st.session_state.bc.chain) > 1:
    block_to_hack = st.number_input("Номер блока для взлома:", min_value=1, max_value=len(st.session_state.bc.chain)-1, step=1)
    if st.button("🚨 Взломать выбранный блок"):
        st.session_state.bc.chain[block_to_hack].transactions = ["⚠️ ДАННЫЕ ПОДМЕНЕНЫ!"]
        st.rerun()
else:
    st.info("Добавьте хотя бы один блок (кроме Генезиса), чтобы разблокировать систему тестирования атак.")
if len(st.session_state.bc.chain) > 1:
    block_to_hack = st.number_input("Номер блока для взлома:", min_value=1, max_value=len(st.session_state.bc.chain)-1, step=1)
    if st.button("🚨 Взломать выбранный блок"):
        st.session_state.bc.chain[block_to_hack].transactions = ["⚠️ ДАННЫЕ ПОДМЕНЕНЫ!"]
        st.rerun()
else:
    st.info("Добавьте хотя бы один блок (кроме Генезиса), чтобы разблокировать систему тестирования атак.")
with col2:
    st.write("### Визуализация цепочки")
    
    is_valid, error_index = st.session_state.blockchain.is_chain_valid()
    
    if is_valid:
        st.success("✅ Состояние системы: Valid (Цепь верна)")
    else:
        st.error(f"❌ Состояние системы: Invalid (Ошибка в блоке №{error_index})")
        st.info("Причина: Нарушение хеш-суммы или разрыв связи")

    for block in reversed(st.session_state.blockchain.chain):
        with st.expander(f"Блок №{block.index} [{'Genesis' if block.index==0 else 'Data'}]"):
            st.code(f"""
Index: {block.index}
Timestamp: {block.timestamp}
Data: {block.transactions}
Prev Hash: {block.previous_hash}
Hash: {block.hash}
            """)

# Футер
st.markdown("---")
st.caption("CryptoGuard Ledger — Готовое коммерческое решение для аудита данных.")
