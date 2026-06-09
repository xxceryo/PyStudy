<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ApiError } from '../api'
import { auth } from '../auth'

const router = useRouter()
const username = ref('')
const nickname = ref('')
const password = ref('')
const passwordConfirmation = ref('')
const errorMessage = ref('')
const submitting = ref(false)

async function submit(): Promise<void> {
  errorMessage.value = ''
  if (password.value !== passwordConfirmation.value) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  submitting.value = true
  try {
    await auth.register({
      username: username.value,
      nickname: nickname.value,
      password: password.value,
    })
    await router.push({ name: 'login', query: { registered: '1' } })
  } catch (error) {
    errorMessage.value = error instanceof ApiError ? error.message : '无法连接到市场服务器'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <main class="auth-page register-page">
    <section class="auth-story">
      <div class="brand-lockup"><span class="brand-mark">LS</span> LOOT//SHIFT</div>
      <div class="story-copy">
        <p class="eyebrow">NEW PLAYER INITIALIZATION</p>
        <h1>加入市场。<br><span>开始交换。</span></h1>
        <p class="story-text">创建唯一玩家档案。商城功能仍在构建中，你将成为第一批进入市场的交易者。</p>
      </div>
      <div class="rarity-stack"><i></i><i></i><i></i><span>RARITY INDEX // 03</span></div>
    </section>

    <section class="auth-panel">
      <div class="panel-inner">
        <p class="panel-code">CREATE PROFILE // 02</p>
        <h2>创建玩家档案</h2>
        <p class="panel-intro">设置你的市场身份与访问密码。</p>
        <p v-if="errorMessage" class="notice error">{{ errorMessage }}</p>
        <form @submit.prevent="submit">
          <div class="field-grid">
            <label>
              <span>用户名</span>
              <input v-model.trim="username" autocomplete="username" minlength="3" maxlength="50" required placeholder="唯一登录代号">
            </label>
            <label>
              <span>昵称</span>
              <input v-model.trim="nickname" autocomplete="nickname" minlength="1" maxlength="50" required placeholder="市场展示名称">
            </label>
          </div>
          <label>
            <span>密码</span>
            <input v-model="password" type="password" autocomplete="new-password" minlength="8" maxlength="72" required placeholder="至少 8 个字符">
          </label>
          <label>
            <span>确认密码</span>
            <input v-model="passwordConfirmation" type="password" autocomplete="new-password" minlength="8" maxlength="72" required placeholder="再次输入密码">
          </label>
          <button class="primary-button" :disabled="submitting" type="submit">
            {{ submitting ? '创建中...' : '创建账号' }} <span>＋</span>
          </button>
        </form>
        <p class="switch-copy">已有玩家档案？ <RouterLink to="/login">返回登录</RouterLink></p>
      </div>
    </section>
  </main>
</template>
