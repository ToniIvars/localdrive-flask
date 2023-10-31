const deleteModal = document.getElementById('delete-modal')
const renameModal = document.getElementById('rename-modal')
const newFolderModal = document.getElementById('new-folder-modal')
const moveItemModal = document.getElementById('move-item-modal')

function customizeModal(DOMItem) {
  DOMItem?.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget
    const itemName = button.closest('.dropdown').getAttribute('data-item-name')

    const modalItemName = DOMItem.querySelector('[data-replace="item-name"]')
    const modalHiddenInput = DOMItem.querySelector('input[type="hidden"]')

    modalItemName.textContent = itemName
    modalHiddenInput.value = itemName
  })
}

function focusTextInput(DOMItem) {
  DOMItem?.addEventListener('show.bs.modal', () => {
    const modalTextInput = DOMItem.querySelector('input[type="text"]')
    setTimeout(() => {
      modalTextInput.focus({ focusVisible: true })
    }, 500);
  })
}

customizeModal(deleteModal)
customizeModal(renameModal)
customizeModal(moveItemModal)

focusTextInput(renameModal)
focusTextInput(newFolderModal)