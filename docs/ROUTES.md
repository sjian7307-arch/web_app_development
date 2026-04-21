# 路由設計文件 (API Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁 (活動列表) | GET | `/` | `templates/events/index.html` | 顯示所有活動清單 |
| 新增活動頁面 | GET | `/events/new` | `templates/events/new.html` | 顯示建立活動表單 |
| 建立活動 | POST | `/events` | — | 接收表單，存入 DB，重導向至活動列表 |
| 活動詳情 | GET | `/events/<id>` | `templates/events/detail.html` | 顯示活動詳情與行程表 |
| 活動報名頁面 | GET | `/events/<id>/register` | `templates/registrations/new.html` | 顯示報名表單 |
| 處理活動報名 | POST | `/events/<id>/register` | `templates/registrations/result.html` | 接收報名資料，顯示成功或失敗結果 |
| 報名名單管理 | GET | `/events/<id>/registrations` | `templates/registrations/index.html` | 主辦方查看報名名單與繳費狀態 |
| 更新繳費狀態 | POST | `/registrations/<id>/payment` | — | 更新繳費狀態，重導向回名單管理頁面 |

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **輸入**: 無
- **處理邏輯**: 呼叫 `Event.get_all()` 取得所有活動
- **輸出**: 渲染 `events/index.html`，傳入活動列表變數

### `GET /events/new`
- **輸入**: 無
- **處理邏輯**: 無
- **輸出**: 渲染 `events/new.html`

### `POST /events`
- **輸入**: 表單欄位 `title`, `description`, `schedule`, `capacity`
- **處理邏輯**: 驗證必填欄位，呼叫 `Event.create(...)`
- **輸出**: 成功後重導向至 `/`

### `GET /events/<id>`
- **輸入**: URL 參數 `id`
- **處理邏輯**: 呼叫 `Event.get_by_id(id)`，若找不到回傳 404
- **輸出**: 渲染 `events/detail.html`，傳入活動詳情

### `GET /events/<id>/register`
- **輸入**: URL 參數 `id`
- **處理邏輯**: 呼叫 `Event.get_by_id(id)`，檢查是否額滿 (`Registration.count_by_event_id(id) >= capacity`)。若額滿，可顯示額滿訊息。
- **輸出**: 渲染 `registrations/new.html`

### `POST /events/<id>/register`
- **輸入**: URL 參數 `id`，表單欄位 `participant_name`, `email`, `phone`
- **處理邏輯**: 
  - 驗證必填欄位
  - 再次檢查是否額滿 (避免同時送出的防護)
  - 呼叫 `Registration.create(...)`
- **輸出**: 渲染 `registrations/result.html` 並傳入結果訊息（報名成功或失敗）

### `GET /events/<id>/registrations`
- **輸入**: URL 參數 `id`
- **處理邏輯**: 呼叫 `Event.get_by_id(id)` 與 `Registration.get_by_event_id(id)` 取得該活動所有報名紀錄
- **輸出**: 渲染 `registrations/index.html`

### `POST /registrations/<id>/payment`
- **輸入**: URL 參數 `id`，表單欄位 `payment_status`
- **處理邏輯**: 呼叫 `Registration.update_payment_status(id, payment_status)`
- **輸出**: 重導向回 `GET /events/<event_id>/registrations`

## 3. Jinja2 模板清單

所有頁面預計繼承自 `templates/base.html`，以保持共同的導覽列與一致的設計系統樣式。

1. **`base.html`**: 共用版型（包含 Header、Footer、CSS 引入）
2. **`events/index.html`**: 首頁，展示活動卡片列表
3. **`events/new.html`**: 建立活動的表單頁面
4. **`events/detail.html`**: 活動詳細資訊與行程表
5. **`registrations/new.html`**: 參加者填寫報名資料的表單
6. **`registrations/result.html`**: 報名提交後的結果通知頁面
7. **`registrations/index.html`**: 後台管理頁面，以表格呈現報名名單與繳費狀態切換
