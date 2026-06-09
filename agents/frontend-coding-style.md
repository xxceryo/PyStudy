# Vue 与 TypeScript 编码规范

- 使用 Vue 3 Composition API 和 `<script setup lang="ts">` 编写新组件。
- 为组件属性、事件、函数参数和返回值提供明确的 TypeScript 类型，避免无必要的 `any`。
- 组件保持单一职责；仅在出现明确复用需求时提取 composable、组件或工具模块。
- 使用清晰、具体的英文名称；Vue 组件文件使用 PascalCase，普通 TypeScript 模块使用 camelCase。
- 模板保持简洁；复杂条件、数据转换和副作用放入脚本逻辑。
- 样式默认使用组件作用域，只有确有跨组件共享需求时才引入全局样式。
- 优先使用 Vue 和浏览器现有能力，不为当前需求之外的假设场景提前增加依赖或抽象。
- 不手工编辑 `frontend/node_modules/` 或 `frontend/dist/` 中的生成内容。
