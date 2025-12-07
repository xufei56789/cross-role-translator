<script setup>
  import { ref } from 'vue'
  
  const roles = [
    { value: 'product_manager', label: '产品经理' },
    { value: 'developer', label: '开发工程师' },
    { value: 'designer', label: '设计师' },
    { value: 'operator', label: '运营人员' },
    { value: 'executive', label: '管理层' },
  ]
  
  const backendBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  
  const sourceRole = ref('product_manager')
  const targetRole = ref('developer')
  const content = ref('')
  
  const loading = ref(false)
  const error = ref('')
  const result = ref(null)
  
  const handleTranslate = async () => {
    error.value = ''
    result.value = null
  
    if (!content.value.trim()) {
      error.value = '请输入要翻译的内容'
      return
    }
  
    loading.value = true
    try {
      const resp = await fetch(`${backendBaseUrl}/api/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          source_role: sourceRole.value,
          target_role: targetRole.value,
          content: content.value,
        }),
      })
  
      if (!resp.ok) {
        const text = await resp.text()
        throw new Error(text || `请求失败：${resp.status}`)
      }
  
      const data = await resp.json()
      result.value = data
    } catch (e) {
      console.error(e)
      error.value = e.message || '请求出错'
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <template>
    <div class="page">
      <header class="header">
        <h1>跨职能沟通翻译助手</h1>
        <p class="subtitle">帮助你把“产品话 / 技术话 / 运营话”翻译成对方听得懂的语言</p>
      </header>
  
      <main class="main">
        <section class="card input-card">
          <h2>输入</h2>
  
          <div class="row">
            <div class="field">
              <label>你的角色</label>
              <select v-model="sourceRole">
                <option v-for="r in roles" :key="r.value" :value="r.value">
                  {{ r.label }}
                </option>
              </select>
            </div>
  
            <div class="field">
              <label>目标角色</label>
              <select v-model="targetRole">
                <option v-for="r in roles" :key="r.value" :value="r.value">
                  {{ r.label }}
                </option>
              </select>
            </div>
          </div>
  
          <div class="field">
            <label>你想表达的内容</label>
            <textarea
              v-model="content"
              rows="8"
              placeholder="例如：我们需要做一个首页智能推荐功能，提高用户停留时长和二跳率，希望下个月能上线..."
            />
          </div>
  
          <button class="primary-btn" :disabled="loading" @click="handleTranslate">
            {{ loading ? '翻译中...' : '开始翻译' }}
          </button>
  
          <p v-if="error" class="error">{{ error }}</p>
        </section>
  
        <section class="card output-card">
          <h2>需求智能翻译</h2>
  
          <div v-if="!result" class="placeholder">
            <p>在左侧输入内容并点击“开始翻译”，这里会显示转换结果。</p>
          </div>
  
          <div v-else class="result">
            <div class="result-intro">
              <p>以下是根据您的输入内容，系统自动分析并生成的跨角色沟通翻译报告：</p>
            </div>

            <div class="result-block">
              <h3>检测到的需求</h3>
              <p>{{ result.detected_scene }}</p>
            </div>

            <div class="result-block">
              <h3>翻译内容</h3>
              <p class="translated">
                {{ result.translated_message }}
              </p>
            </div>

            <div class="result-block">
              <h3>智能分析</h3>
              <ul v-if="result.info_completion?.length">
                <li v-for="(item, idx) in result.info_completion" :key="idx">
                  <strong>{{ item.item }}</strong>
                  <span class="tag">{{ item.status }}</span>
                  <div v-if="item.suggested_value" class="hint">
                    建议值/推断：{{ item.suggested_value }}
                  </div>
                </li>
              </ul>
              <p v-else>暂无明显需要补充的信息。</p>
            </div>

            <div class="result-block">
              <h3>分险提示</h3>
              <ul v-if="result.risk_alerts?.length">
                <li v-for="(r, idx) in result.risk_alerts" :key="idx">
                  {{ r }}
                </li>
              </ul>
              <p v-else>未发现明显风险点。</p>
            </div>

            <div class="result-block">
              <h3>建议</h3>
              <p>{{ result.suggestion_for_source }}</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  </template>
  
  <style scoped>
  .page {
    min-height: 100vh;
    background: #f6f7fb;
    padding: 24px;
    box-sizing: border-box;
  }
  
  .header {
    max-width: 960px;
    margin: 0 auto 16px;
  }
  
  .header h1 {
    margin: 0;
    font-size: 26px;
  }
  
  .subtitle {
    margin-top: 4px;
    color: #666;
    font-size: 14px;
  }
  
  .main {
    max-width: 960px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1.1fr 1.4fr;
    gap: 16px;
  }
  
  .card {
    background: #fff;
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 4px 12px rgba(15, 35, 52, 0.06);
    display: flex;
    flex-direction: column;
  }
  
  .card h2 {
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 18px;
  }
  
  .row {
    display: flex;
    gap: 12px;
    margin-bottom: 8px;
  }
  
  .field {
    display: flex;
    flex-direction: column;
    flex: 1;
    margin-bottom: 8px;
  }
  
  .field label {
    font-size: 13px;
    color: #555;
    margin-bottom: 4px;
  }
  
  select,
  textarea {
    border-radius: 8px;
    border: 1px solid #ddd;
    padding: 6px 8px;
    font-size: 14px;
    outline: none;
    resize: vertical;
  }
  
  select:focus,
  textarea:focus {
    border-color: #409eff;
  }
  
  .primary-btn {
    align-self: flex-start;
    margin-top: 8px;
    padding: 6px 16px;
    border-radius: 999px;
    border: none;
    background: #409eff;
    color: #fff;
    font-size: 14px;
    cursor: pointer;
  }
  
  .primary-btn:disabled {
    opacity: 0.7;
    cursor: default;
  }
  
  .error {
    color: #e03f3f;
    font-size: 13px;
    margin-top: 6px;
  }
  
  .placeholder {
    color: #888;
    font-size: 14px;
  }
  
  .result-intro {
    margin-bottom: 20px;
    padding: 14px 16px;
    background: linear-gradient(135deg, #f0f4ff 0%, #e8edff 100%);
    border-radius: 10px;
    border-left: 4px solid #335eea;
    box-shadow: 0 2px 8px rgba(51, 94, 234, 0.1);
  }
  
  .result-intro p {
    margin: 0;
    color: #333;
    font-size: 14px;
    line-height: 1.6;
    font-weight: 500;
  }
  
  .result-block {
    margin-bottom: 20px;
    background: #ffffff;
    border: 1px solid #e5e9f2;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .result-block::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #335eea 0%, #5b7cfa 100%);
  }
  
  .result-block:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-1px);
  }
  
  .result-block:last-child {
    margin-bottom: 0;
  }
  
  .result-block h3 {
    font-size: 16px;
    margin: 0 0 12px 0;
    color: #1a1a1a;
    font-weight: 600;
    padding-bottom: 8px;
    border-bottom: 2px solid #f0f4ff;
    display: flex;
    align-items: center;
  }
  
  .result-block h3::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 16px;
    background: #335eea;
    border-radius: 2px;
    margin-right: 8px;
  }
  
  .result-block p {
    margin: 0;
    color: #4a5568;
    font-size: 14px;
    line-height: 1.8;
  }
  
  .translated {
    white-space: pre-wrap;
    background: #f8f9fa;
    padding: 14px;
    border-radius: 8px;
    border: 1px solid #e9ecef;
    color: #2d3748;
    line-height: 1.8;
    font-size: 14px;
  }
  
  .result-block ul {
    padding-left: 0;
    margin: 8px 0 0 0;
    list-style: none;
  }
  
  .result-block li {
    margin-bottom: 12px;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 6px;
    border-left: 3px solid #dee2e6;
    transition: all 0.2s ease;
  }
  
  .result-block li:hover {
    background: #f0f4ff;
    border-left-color: #335eea;
  }
  
  .result-block li:last-child {
    margin-bottom: 0;
  }
  
  .tag {
    display: inline-block;
    margin-left: 8px;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
    background: linear-gradient(135deg, #f0f4ff 0%, #e8edff 100%);
    color: #335eea;
    border: 1px solid rgba(51, 94, 234, 0.2);
  }
  
  .hint {
    font-size: 13px;
    color: #666;
    margin-top: 6px;
    padding: 6px 10px;
    background: #fff;
    border-radius: 4px;
    border: 1px dashed #cbd5e0;
  }
  
  @media (max-width: 768px) {
    .main {
      grid-template-columns: 1fr;
    }
  }
  </style>