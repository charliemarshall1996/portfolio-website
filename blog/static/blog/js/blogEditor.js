class BlogEditor {
  constructor() {
    this.blocks = [];
    this.quillInstances = new Map();
    this.initialize();
  }

  initialize() {
    this.loadInitialData();
    this.renderBlocks();
    this.setupEventListeners();
  }

  loadInitialData() {
    const bodyInput = document.getElementById("id_body");
    if (bodyInput && bodyInput.value) {
      try {
        this.blocks = JSON.parse(bodyInput.value);
      } catch (error) {
        console.error("Error parsing initial stream data:", error);
      }
    }
  }

  setupEventListeners() {
    document.addEventListener("click", (e) => {
      if (e.target.closest('[data-action="add-block"]')) {
        const type = e.target.dataset.blockType;
        this.addBlock(type);
      }
    });
  }

  addBlock(type) {
    const newBlock = {
      id: Date.now(),
      type: type,
      value: this.getDefaultValueForType(type),
    };

    this.blocks.push(newBlock);
    this.renderBlocks();
  }

  getDefaultValueForType(type) {
    switch (type) {
      case "paragraph":
        return "";
      case "image":
        return { id: null, alt: "" }; // Adjust based on your image handling
      case "code":
        return { language: "python", code: "" };
      case "raw_html":
        return "";
      default:
        return "";
    }
  }

  updateBlockValue(blockId, newValue) {
    const block = this.blocks.find((b) => b.id === blockId);
    if (block) {
      block.value = newValue;
      this.updateHiddenField();
    }
  }

  updateCodeBlock(blockId, field, value) {
    const block = this.blocks.find((b) => b.id === blockId);
    if (block && block.type === "code") {
      block.value[field] = value;
      this.updateHiddenField();
    }
  }

  updateImageBlock(blockId, field, value) {
    const block = this.blocks.find((b) => b.id === blockId);
    if (block && block.type === "image") {
      block.value[field] = value;
      this.updateHiddenField();
    }
  }

  deleteBlock(blockId) {
    this.blocks = this.blocks.filter((b) => b.id !== blockId);
    this.renderBlocks();
  }

  renderBlocks() {
    const container = document.getElementById("blocks-container");
    container.innerHTML = "";

    this.blocks.forEach((block) => {
      const blockElement = this.createBlockElement(block);
      container.appendChild(blockElement);
    });

    this.updateHiddenField();
  }

  createBlockElement(block) {
    const wrapper = document.createElement("div");
    wrapper.className = "stream-block";
    wrapper.innerHTML = `
            <div class="block-header">
                <button class="delete-block btn btn-danger" data-block-id="${
                  block.id
                }">Delete</button>
            </div>
            <div class="block-content">
                ${this.getBlockContent(block)}
            </div>
        `;

    wrapper.querySelector(".delete-block").addEventListener("click", () => {
      this.deleteBlock(block.id);
    });

    return wrapper;
  }

  getBlockContent(block) {
    switch (block.type) {
      case "paragraph":
        return `
          <div class="rich-text-editor-container form-control" data-block-id="${block.id}">
            <div id="editor-${block.id}" class="rich-text-editor"></div>
          </div>
        `;

      case "captioned_image":
        return `
          <div class="image-uploader card p-3 mb-3">
            <div class="input-group mb-2">
              <input type="file" 
                data-block-id="${block.id}"
                class="image-file-input form-control"
                accept="image/*"
              >
            </div>
            <input type="text"
              class="image-alt-text form-control"
              data-block-id="${block.id}"
              placeholder="Alt text"
              value="${block.value.alt}"
            >
            <input type="text"
              class="image-alt-text form-control"
              data-block-id="${block.id}"
              placeholder="Caption"
              value="${block.value.alt}"
            >
          </div>
        `;

      case "image":
        return `
          <div class="image-uploader card p-3 mb-3">
            <div class="input-group mb-2">
              <input type="file" 
                data-block-id="${block.id}"
                class="image-file-input form-control"
                accept="image/*"
              >
            </div>
            <input type="text"
              class="image-alt-text form-control"
              data-block-id="${block.id}"
              placeholder="Caption"
              value="${block.value.alt}"
            >
          </div>
        `;

      case "code":
        return `
          <div class="code-block card p-3 mb-3">
            <div class="input-group mb-2">
              <select class="code-language form-select" data-block-id="${
                block.id
              }">
                ${["python", "javascript", "html", "css", "bash"]
                  .map(
                    (lang) =>
                      `<option value="${lang}" ${
                        block.value.language === lang ? "selected" : ""
                      }>${lang}</option>`
                  )
                  .join("")}
              </select>
            </div>
            <textarea 
              class="code-content form-control font-monospace" 
              data-block-id="${block.id}"
              placeholder="Enter code..."
              style="height: 150px"
            >${block.value.code}</textarea>
          </div>
        `;

      case "raw_html":
        return `
          <textarea 
            class="html-editor form-control font-monospace" 
            data-block-id="${block.id}"
            placeholder="Enter HTML..."
            style="height: 150px"
          >${block.value}</textarea>
        `;

      default:
        return "";
    }
  }

  renderBlocks() {
    const container = document.getElementById("blocks-container");
    container.innerHTML = "";

    this.blocks.forEach((block) => {
      const blockElement = this.createBlockElement(block);
      container.appendChild(blockElement);
      this.initializeRichTextEditor(block);
    });

    this.updateHiddenField();
  }

  initializeRichTextEditor(block) {
    if (block.type === "paragraph") {
      const editorId = `editor-${block.id}`;
      const toolbarOptions = [
        ["bold", "italic", "underline", "strike"],
        ["blockquote", "code-block"],
        [{ header: 1 }, { header: 2 }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ script: "sub" }, { script: "super" }],
        ["link", "image"],
        ["clean"],
      ];

      const quill = new Quill(`#${editorId}`, {
        modules: {
          toolbar: toolbarOptions,
        },
        theme: "snow",
      });

      quill.root.innerHTML = block.value;

      quill.on("text-change", () => {
        this.updateBlockValue(block.id, quill.root.innerHTML);
      });

      this.quillInstances.set(block.id, quill);
    }
  }

  updateHiddenField() {
    const bodyInput = document.getElementById("id_body");
    if (bodyInput) {
      bodyInput.value = JSON.stringify(this.blocks);
    }
  }

  deleteBlock(blockId) {
    this.blocks = this.blocks.filter((b) => b.id !== blockId);
    const quill = this.quillInstances.get(blockId);
    if (quill) {
      quill.destroy();
      this.quillInstances.delete(blockId);
    }
    this.renderBlocks();
  }
}

// Initialize the editor when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.blogEditor = new BlogEditor();
});
