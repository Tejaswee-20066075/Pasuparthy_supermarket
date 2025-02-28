document.addEventListener("DOMContentLoaded", function() {
    fetchProducts();
});

function fetchProducts() {
    fetch("http://127.0.0.1:5000/products")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#inventoryTable tbody");
            tableBody.innerHTML = "";
            data.forEach(product => {
                let row = `<tr>
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.category}</td>
                    <td>${product.quantity}</td>
                    <td>${product.price}</td>
                    <td>${product.expiry_date}</td>
                    <td>${product.supplier}</td>
                    <td>
                        <a href="edit.html?id=${product.id}">Edit</a> |
                        <button onclick="deleteProduct(${product.id})">Delete</button>
                    </td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        });
}

function deleteProduct(id) {
    fetch(`http://127.0.0.1:5000/products/${id}`, { method: "DELETE" })
        .then(response => response.json())
        .then(() => fetchProducts());
}
