async function loadBooks() {
  try {
    const response = await fetch("assets/data/books.json");
    if (!response.ok) {
      throw new Error("Failed to load books.");
    }
    const books = await response.json();
    populateBooks(books);
  } catch (error) {
    console.error("Error loading books:", error);
  }
}

function populateBooks(books) {
  const grid = document.getElementById("books-grid");
  books.forEach((book, index) => {
    const item = document.createElement("div");
    item.classList.add("grid-item");

    const img = document.createElement("img");
    img.src = book.cover;
    img.alt = book.title;

    const navWrapper = document.createElement("div");

    const nav = document.createElement("nav");
    const ul = document.createElement("ul");
    const li = document.createElement("li");

    const link = document.createElement("a");
    link.href = "#";
    link.textContent = "Meer";

    link.style.fontSize = "0.8rem";
    link.style.padding = "0.3rem 0.6rem";
    link.style.textDecoration = "none";
    link.style.backgroundColor = "#e63838";
    link.style.color = "#fff";
    link.style.borderRadius = "2em";
    link.style.display = "inline-block";
    link.style.textAlign = "center";
    link.style.width = "100%";
    link.style.boxSizing = "border-box";

    link.addEventListener("mouseover", () => {
      link.style.backgroundColor = "#a22929";
    });

    link.addEventListener("mouseout", () => {
      link.style.backgroundColor = "#e63838";
    });

    link.addEventListener("click", (event) => {
      event.preventDefault();
      showModal(book);
    });

    li.appendChild(link);
    ul.appendChild(li);
    nav.appendChild(ul);
    navWrapper.appendChild(nav);

    item.appendChild(img);
    item.appendChild(navWrapper);
    grid.appendChild(item);
  });
}

function showModal(book) {
  const modal = document.getElementById("book-modal");
  const modalTitle = modal.querySelector(".modal-title");
  const modalBody = modal.querySelector(".modal-body");

  modalTitle.textContent = book.title;
  modalBody.textContent = book.description;

  modal.style.display = "block";

  modal.addEventListener("click", (event) => {
    const modalContent = modal.querySelector(".modal-content");
    if (!modalContent.contains(event.target)) {
      closeModal();
    }
  });
}

function closeModal() {
  const modal = document.getElementById("book-modal");
  modal.style.display = "none";
}

window.onload = () => {
  loadBooks();

  document.getElementById("modal-close").addEventListener("click", closeModal);
};