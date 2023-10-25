const deleteModal = document.getElementById('delete-modal')
const renameModal = document.getElementById('rename-modal')

function customizeModal(DOMItem) {
  if (DOMItem) {
    DOMItem.addEventListener('show.bs.modal', event => {
      const button = event.relatedTarget
      const itemName = button.closest('.dropdown').getAttribute('data-item-name')

      const modalItemName = DOMItem.querySelector('[data-replace="item-name"]')
      const modalHiddenInput = DOMItem.querySelector('input[type="hidden"]')

      modalItemName.textContent = itemName
      modalHiddenInput.value = itemName
    })
  }
}

customizeModal(deleteModal)
customizeModal(renameModal)