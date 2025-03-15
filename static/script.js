document.addEventListener("DOMContentLoaded", function () {
    fetchProducts();
});

/** ✅ Fetch and Display Products */
async function fetchProducts() {
    try {
        const response = await fetch("/products");
        if (!response.ok) throw new Error("Failed to fetch products");

        const data = await response.json();
        const tableBody = document.querySelector("#inventoryTable tbody");
        tableBody.innerHTML = "";

        data.forEach(product => {
            let row = `<tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.category}</td>
                <td>${product.quantity}</td>
                <td>${product.price.toFixed(2)}</td>
                <td>${product.expiry_date || "N/A"}</td>
                <td>${product.supplier}</td>
                <td>
                    <a href="{{ url_for('edit_page', product_id=${product.id}) }}">✏️ Edit</a>| 
                    <button onclick="deleteProduct(${product.id})">🗑️ Delete</button>
                </td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error("Error loading products:", error);
    }
}

/** ✅ Delete a Product (With Confirmation) */
async function deleteProduct(id) {
    if (!confirm(`Are you sure you want to delete Product ID ${id}?`)) return;

    try {
        const response = await fetch(`/products/${id}`, { method: "DELETE" });
        if (!response.ok) throw new Error("Failed to delete product");

        alert("Product deleted successfully!");
        fetchProducts(); // Refresh the list
    } catch (error) {
        console.error("Error deleting product:", error);
        alert("Error deleting product. Please try again.");
    }
}

/** ✅ Add New Product */
async function addProduct(event) {
    event.preventDefault();

    const product = {
        name: document.getElementById("name").value.trim(),
        category: document.getElementById("category").value.trim(),
        quantity: parseInt(document.getElementById("quantity").value),
        price: parseFloat(document.getElementById("price").value),
        expiry_date: document.getElementById("expiry_date").value || null,
        supplier: document.getElementById("supplier").value.trim()
    };

    try {
        const response = await fetch("/products", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(product)
        });

        if (!response.ok) throw new Error("Failed to add product");

        alert("Product added successfully!");
        fetchProducts();
        document.getElementById("productForm").reset();
    } catch (error) {
        console.error("Error adding product:", error);
        alert("Error adding product. Please try again.");
    }
}

// ✅ Attach event listener (Only if form exists)
const productForm = document.getElementById("productForm");
if (productForm) {
    productForm.addEventListener("submit", addProduct);
}

/** ✅ Edit Product (Fetch & Update Data) */
async function editProduct(event) {
    event.preventDefault();
    const productId = document.getElementById("editId").value;

    const updatedProduct = {
        name: document.getElementById("editName").value.trim(),
        category: document.getElementById("editCategory").value.trim(),
        quantity: parseInt(document.getElementById("editQuantity").value),
        price: parseFloat(document.getElementById("editPrice").value),
        expiry_date: document.getElementById("editExpiry").value || null,
        supplier: document.getElementById("editSupplier").value.trim()
    };

    try {
        const response = await fetch(`/products/${productId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedProduct)
        });

        if (!response.ok) throw new Error("Failed to update product");

        alert("Product updated successfully!");
        window.location.href = "/";
    } catch (error) {
        console.error("Error updating product:", error);
        alert("Error updating product. Please try again.");
    }
}

// ✅ Attach event listener (Only if form exists)
const editForm = document.getElementById("editForm");
if (editForm) {
    editForm.addEventListener("submit", editProduct);
}

