# zhouzk.com（Astro 版本）

使用 [Astro 5](https://astro.build) 重构的个人网站，涵盖首页、文章、工具等内容模块，并通过 Content Collections + Markdown 管理文章。

## 目录结构

```text
.
├── public/                 # 静态资源（包含 legacy CSS、图片等）
├── src/
│   ├── components/         # NavBar、Footer、LanguageSwitcher、ArticleCard
│   ├── content/            # Markdown 文章与 collection schema
│   ├── layouts/            # BaseLayout、ArticleLayout
│   └── pages/              # 首页、文章列表、文章详情、工具页
├── legacy_site/            # 旧版静态 HTML 备份
├── astro.config.mjs        # Astro 配置（含站点信息）
└── package.json
```

## 开发与构建

```bash
npm install        # 安装依赖
npm run dev        # 本地开发（默认 4321 端口）
npm run build      # 生成静态站点到 dist/
npm run preview    # 预览构建结果
```

## 内容管理

- 所有文章位于 `src/content/articles/`，使用 Markdown + Frontmatter。
- `src/content/config.ts` 定义了 `articles` collection（标题、描述、日期、标签、FAQ 等）。
- 新增文章：复制现有 Markdown，调整 Frontmatter 与正文即可。

## 样式与资源

- 公共样式保留在 `public/assets/css/common.css`。
- 页面的局部样式通过对应 `.astro` 或 `.md` 文件中的 `<style>` 标签维护。
- Font Awesome、Google Analytics 等第三方依赖在 `BaseLayout.astro` 中统一引入。

## 运行要求

- Node.js 18+
- 推荐包管理器：npm（也可使用 pnpm/yarn，需自行配置 lockfile）
