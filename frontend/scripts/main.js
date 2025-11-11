import ApiService from "../services/api-service.js";

const itemList = document.getElementById("itemList");
const addItemBtn = document.getElementById("addItemBtn");
const modal = document.getElementById("itemModal");
const closeModalBtn = document.getElementById("closeModalBtn");
const itemForm = document.getElementById("itemForm");
const modalTitle = document.getElementById("modalTitle");

let editItemName = null;

// Load items when page loads
document.addEventListener("DOMContentLoaded", () => {
  loadItems();
});


async function loadItems() {
  try {
    const response = await ApiService.get("/inventory/");
    const items = response.data || []; // Extract actual array
    renderItems(items);
  } catch (error) {
    console.error("Error fetching items:", error);
    itemList.innerHTML = `<p class="error-text">Failed to load items.</p>`;
  }
}


// ✅ Render all items
function renderItems(items = []) {
  if (!items.length) {
    itemList.innerHTML = `<p>No items found. Add a new one!</p>`;
    return;
  }

  itemList.innerHTML = items
    .map(
      (item) => `
        <div class="item-card">
          <div class="item-info">
            <h3>${escapeHtml(item.item_name)}</h3>
            <p><strong>Category:</strong> ${escapeHtml(item.cat_name)}</p>
            <p><strong>Status:</strong> ${escapeHtml(item.item_status)}</p>
            <p><strong>Comment:</strong> ${escapeHtml(item.comment || "—")}</p>
            <p><strong>User:</strong> ${escapeHtml(item.username || "—")}</p>
          </div>
          <div class="item-actions">
            <button class="btn-delete" data-name="${escapeAttr(item.item_name)}">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>
      `
    )
    .join("");

  // Add delete listeners
    // Add delete listeners
    document.querySelectorAll(".btn-delete").forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        const itemName = e.currentTarget.dataset.name;
        const confirmed = await customConfirm(`Delete item "${itemName}"?`);
        if (confirmed) {
          await deleteItem(itemName);
        }
      });
    });  
}

// ✅ Open and close modal
addItemBtn.addEventListener("click", () => openModal());
closeModalBtn.addEventListener("click", () => closeModal());

function openModal() {
  modal.style.display = "flex";
  modalTitle.textContent = "Add New Item";
  itemForm.reset();
}

function closeModal() {
  modal.style.display = "none";
  editItemName = null;
}

// ✅ Save new item
itemForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const itemData = {
    item_name: document.getElementById("item_name").value.trim(),
    cat_name: document.getElementById("cat_name").value.trim(),
    item_status: document.getElementById("item_status").value,
    comment: document.getElementById("comment").value.trim(),
    username: document.getElementById("username").value.trim(),
  };

  try {
    await ApiService.post("/inventory/", itemData);
    alert("Item saved successfully!");
    closeModal();
    loadItems();
  } catch (error) {
    console.error("Error saving item:", error);
    alert("Error saving item: " + error.message);
  }
});

// ✅ Delete item
async function deleteItem(itemName) {
  try {
    await ApiService.delete(`/inventory/${encodeURIComponent(itemName)}`);
    alert("Item deleted successfully!");
    loadItems();
  } catch (error) {
    console.error("Error deleting item:", error);
    alert("Failed to delete item.");
  }
}

// ✅ Click outside modal closes it
window.onclick = function (event) {
  if (event.target === modal) closeModal();
};

// ✅ Safe HTML output
function escapeHtml(str = "") {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeAttr(str = "") {
  return String(str).replaceAll('"', "&quot;");
}

// ✅ Custom confirmation popup (non-blocking, works in sandbox)
function customConfirm(message) {
  return new Promise((resolve) => {
    const overlay = document.createElement("div");
    overlay.className = "confirm-overlay";

    const box = document.createElement("div");
    box.className = "confirm-box";
    box.innerHTML = `
      <p>${message}</p>
      <div class="confirm-buttons">
        <button id="confirm-yes">Yes</button>
        <button id="confirm-no">No</button>
      </div>
    `;

    overlay.appendChild(box);
    document.body.appendChild(overlay);

    const yes = box.querySelector("#confirm-yes");
    const no = box.querySelector("#confirm-no");

    yes.onclick = () => {
      document.body.removeChild(overlay);
      resolve(true);
    };
    no.onclick = () => {
      document.body.removeChild(overlay);
      resolve(false);
    };
  });
}
