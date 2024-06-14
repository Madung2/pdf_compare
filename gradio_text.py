import gradio as gr

# HTML 콘텐츠 정의
html_content = """
<div>
  <label for="category">Category</label>
  <select id="category" onchange="updateItemDropdown()">
    <option value="">Select a category</option>
    <option value="Fruits">Fruits</option>
    <option value="Vegetables">Vegetables</option>
  </select>
  
  <label for="item">Item</label>
  <select id="item">
    <option value="">Select an item</option>
  </select>
</div>
"""

# JavaScript 코드 정의
js_code = """
<script>
  const options = {
    "Fruits": ["Apple", "Banana", "Cherry"],
    "Vegetables": ["Carrot", "Lettuce", "Potato"]
  };
  
  function updateItemDropdown() {
    const category = document.getElementById('category').value;
    const itemDropdown = document.getElementById('item');
    itemDropdown.innerHTML = '<option value="">Select an item</option>';
    
    if (category) {
      options[category].forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        itemDropdown.appendChild(option);
      });
    }
  }
</script>
"""

# HTML 블록과 JavaScript 포함
with gr.Blocks() as demo:
    gr.HTML(html_content + js_code)

demo.launch()