import streamlit as st

#shopping list 
shopping_list = [
    ("Fruits", "Apples", 50, "1KG"),
    ("Fruits", "Bananas", 20, "1KG"),
    ("Dairy", "Milk", 60, "1Lit"),
    
    ("Dairy", "Cheese", 150, "1 packet"),
    ("Bakery", "Bread", 40, "1 packet"),
    ("Poultry", "Eggs", 50, "10 nos"),
    ("Vegetables", "Tomatoes", 60, "1KG"),
    ("Vegetables", "Carrots", 50, "1KG"),
    ("Grains", "Rice", 500, "5KG"),
    ("Meat", "Chicken", 200, "1KG")
]

# Initializing cart
if "cart" not in st.session_state:
    st.session_state.cart = []

st.title("Shopping Billing System")

# Sidebar filters
st.sidebar.header("Search and Filter Items")
search = st.sidebar.text_input("Search for an item:")
categories = list(set([item[0] for item in shopping_list]))
selected_category = st.sidebar.selectbox("Filter by category:", ["All"] + categories)

# Filtering
filtered_list = [item for item in shopping_list if search.lower() in item[1].lower()]
if selected_category != "All":
    filtered_list = [item for item in filtered_list if item[0] == selected_category]

# Displaying available items
st.header("Available Items")
if search and not filtered_list:
    st.warning("No items match your search.")
else:
    for idx, (category, name, price, unit) in enumerate(filtered_list or shopping_list, start=1):
        st.write(f"{idx}. **{name}** - ₹{price} ({unit}) [{category}]")

# Adding items to cart
st.header("Add Items to Cart")
if filtered_list or shopping_list:
    item_index = st.selectbox(
        "Select an item:",
        range(len(filtered_list or shopping_list)),
        format_func=lambda i: (filtered_list or shopping_list)[i][1],
    )
    category, item_name, item_price, item_unit = (filtered_list or shopping_list)[item_index]
    quantity = st.number_input(f"Enter quantity for {item_name} ({item_unit}):", min_value=1, step=1)

    if st.button("Add to Cart"):
        cost = item_price * quantity
        for i, (cart_category, cart_item, cart_qty, cart_cost) in enumerate(st.session_state.cart):
            if cart_item == item_name:
                st.session_state.cart[i] = (cart_category, cart_item, cart_qty + quantity, cart_cost + cost)
                break
        else:
            st.session_state.cart.append((category, item_name, quantity, cost))
        st.success(f"{quantity} x {item_name} added to cart!")

# Cart summary
st.sidebar.header("Cart Summary")
total = 0
for item in st.session_state.cart:
    category, name, qty, cost = item
    st.sidebar.write(f"{name}: {qty} x ₹{cost // qty} = ₹{cost}")
    total += cost
st.sidebar.write(f"**Total Amount: ₹{total}**")

# Edit or remove items from cart
if st.session_state.cart:
    st.header("Cart")
    for i, (category, item, qty, cost) in enumerate(st.session_state.cart):
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.write(f"{item}: {qty} x ₹{cost // qty} = ₹{cost}")
        with col2:
            new_qty = st.number_input(f"Qty for {item}", min_value=1, value=qty, key=f"qty_{i}")
        with col3:
            if st.button(f"Remove {item}", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.experimental_rerun()
        if new_qty != qty:
            st.session_state.cart[i] = (category, item, new_qty, new_qty * (cost // qty))

# Checkout
if st.session_state.cart:
    if st.button("Checkout"):
        st.header("Receipt")
        for category, item, qty, cost in st.session_state.cart:
            st.write(f"{item}: {qty} x ₹{cost // qty} = ₹{cost}")
        st.write(f"**Grand Total: ₹{total}**")
        st.balloons()
        st.session_state.cart = []
else:
    st.warning("Your cart is empty. Add some items to proceed.")
