const dropdownMenu = document.querySelector(".dropdown-menu") // for settings
const dropdownButton = document.querySelector(".dropdown-button")
if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  })
}
const photoInput = document.querySelector("#avatar") // upload Image
const photoPreview = document.querySelector("#preview-avatar")
if (photoInput)
  photoInput.onchange = () => {
  const [file] = photoInput.files;
  if (file) {
    photoPreview.src = URL.createObjectURL(file);
  }
}
const conversationThread = document.querySelector(".room__box") // scroll to bottom
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

document.addEventListener("DOMContentLoaded", function () { // going to bottom of news
  const loadMoreButton = document.querySelector(".load-more")
  const roomList = document.querySelector(".roomList")
  const rooms = Array.from(roomList.querySelectorAll(".roomListRoom"))
  const totalRooms = rooms.length
  if (totalRooms <= 3) {
    loadMoreButton.style.display = "none";
  }
  rooms.slice(3).forEach(room => { // hide all rooms beyond the first 3 initially
    room.style.display = "none"
  })
  loadMoreButton.addEventListener("click", function (event) {
    event.preventDefault()
    const visibleRooms = roomList.querySelectorAll(".roomListRoom:not([style='display: none;'])").length
    const totalRooms = rooms.length
    const nextIndex = visibleRooms + 3
    rooms.slice(visibleRooms, nextIndex).forEach(room => {
      room.style.display = "" // show 3 more rooms
    })
    if (nextIndex >= totalRooms) {
      loadMoreButton.style.display = "none"; // hide load more
    }
  })
})
const checkboxes = document.querySelectorAll('input[type="checkbox"]') // for all users/moderators
checkboxes.forEach((checkbox) => {
  checkbox.addEventListener('click', () => {
    document.getElementById('update-moderator-form').submit()
  })
})

