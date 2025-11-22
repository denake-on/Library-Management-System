# Library Management System / 图书馆管理系统

[English](#library-management-system) | [中文](#图书馆管理系统)

## Library Management System

This is a comprehensive Library Management System that provides different interfaces for readers, librarians, and library directors. The system manages book borrowing, returning, renewing, user accounts, and library operations.

### Project Structure

#### Root Directory
- `README.md` - Project documentation file
- `Backend/` - Contains all backend-related files
- `Frontend/` - Contains traditional HTML frontend files, Convert the prototype designed in Figma into corresponding HTML effect files
- `Vue-Frontend/` - Contains Vue.js 3 frontend files, the real Frontend

#### Backend Directory Structure
- `main.py` - The main FastAPI application file containing routing and authentication logic
- `requirements.txt` - Python dependencies list
- `create_librarian_table.py` - Script to initialize librarian table in database
- `library.db` - Backend database file used by the application
- `api/` - Directory containing API route modules
  - `books.py` - API endpoints related to book operations
  - `information.py` - API endpoints for user information management
  - `librarianBookOperation.py` - API endpoints for librarian book operations
  - `librarianReaderOperation.py` - API endpoints for librarian reader operations
  - `director.py` - API endpoints for library director operations
- `venv/` - Python virtual environment directory (if created)

#### Frontend Directory Structure
- `background-animation.js` - JavaScript file for p5.js background animations
- `images/` - Directory containing image assets
- `Reader/` - Directory containing reader-specific HTML pages
  - `login.html` - Reader login page
  - `reader-home.html` - Reader homepage
  - `search-results.html` - Book search results page for readers
  - `my-borrowings.html` - Reader's borrowing history page
  - `profile-edit.html` - Reader profile editing page
  - `calendar.html` - Calendar view for reader activity
- `Librarian/` - Directory containing librarian-specific HTML pages
  - `librarian-home.html` - Librarian homepage
  - `manage-books.html` - Book management page
  - `manage-readers.html` - Reader management page
  - `librarian-profile.html` - Librarian profile page
  - `librarian-book-detail.html` - Book detail page for librarians
  - `librarian-reader-detail.html` - Reader detail page for librarians
  - `librarian-report.html` - Library report page for librarians
- `Library-Director/` - Directory containing library director-specific HTML pages
  - `director-home.html` - Library director homepage
  - `director-manage-books.html` - Book management page for directors
  - `director-manage-readers.html` - Reader management page for directors
  - `director-profile.html` - Director profile page
  - `director-book-detail.html` - Book detail page for directors
  - `director-reader-detail.html` - Reader detail page for directors
  - `director-report.html` - Library report page for directors

#### Vue-Frontend Directory Structure
- `index.html` - Main HTML entry point for Vue application
- `package.json` - Node.js package configuration file
- `package-lock.json` - Node.js lock file for dependency management
- `vite.config.js` - Vite build configuration file
- `src/` - Source code directory for Vue application
  - `main.js` - Main JavaScript entry point for Vue application
  - `App.vue` - Root Vue component
  - `assets/` - Directory containing static assets (images, styles, etc.)
  - `components/` - Directory containing Vue component files

### Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- npm package manager

### Setup and Running

#### Backend Setup

1. Navigate to the Backend directory:
   ```bash
   cd D:\studying\csc3170\LMS\Backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the backend server:
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

The backend server will start on `http://127.0.0.1:8000`. The API endpoints will be available at `http://127.0.0.1:8000/api/`.

#### Frontend Setup

##### Traditional HTML Frontend
The traditional frontend is located in the `Frontend` directory and requires no special setup. You can open the HTML files directly in your browser:
- Reader login: `Frontend/Reader/login.html`
- Librarian interface: `Frontend/Librarian/librarian-home.html`
- Director interface: `Frontend/Library-Director/director-home.html`

##### Vue.js Frontend
1. Navigate to the Vue-Frontend directory:
   ```bash
   cd D:\studying\csc3170\LMS\Vue-Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The Vue frontend will be available at `http://localhost:5173` (or another port if 5173 is in use).

### Architecture

#### Frontend Architecture
The system provides two different frontend implementations:
1. **Traditional HTML/CSS/JavaScript frontend** in the `Frontend` directory
2. **Modern Vue.js 3 frontend** in the `Vue-Frontend` directory

**Traditional Frontend:**
- Separate sections for Readers, Librarians, and Library Directors
- Uses p5.js for animated background effects
- Pure JavaScript implementation with HTML/CSS

**Vue.js Frontend:**
- Built with Vue 3 framework
- Uses Vite as the build tool
- Includes FullCalendar component for calendar views
- Component-based architecture

#### Backend Architecture
- **Framework**: FastAPI (Python)
- **Database**: SQLite3 (located at `Backend/library.db`)
- **Structure**: Multi-layered with main.py handling authentication and routing
- **API Organization**: Separate modules for different functionalities
- **Validation**: Pydantic models for request/response validation
- **Logging**: Comprehensive server-side logging

### Technology Stack

#### Backend
- **Language**: Python 3.x
- **Framework**: FastAPI (0.104.1)
- **Server**: uvicorn (0.24.0)
- **Validation**: Pydantic (2.5.0)
- **Database**: SQLite3 (built-in)
- **Multipart**: python-multipart (0.0.6)

#### Frontend
**Traditional Frontend:**
- **Animation**: p5.js (1.7.0)
- **Languages**: HTML, CSS, JavaScript

**Vue.js Frontend:**
- **Framework**: Vue.js (3.4.21)
- **Build Tool**: Vite (5.2.0)
- **Calendar**: @fullcalendar/vue3 (6.1.19), @fullcalendar/daygrid (6.1.19)
- **Dev Tools**: @vitejs/plugin-vue (5.2.4)

### API Endpoints

#### Authentication Endpoints
- `POST /api/login` - User authentication

#### Health Check
- `GET /health` - System health status

#### Books Endpoints (`/api/`)
- `GET /search-books` - Search books by query
- `GET /reader-borrowings` - Get reader's borrowing history
- `GET /reader-activity-calendar` - Get reading activity calendar
- `POST /borrow-book` - Borrow a book
- `GET /reader-reading-report` - Generate reading report
- `GET /reader-return-books` - Return a book
- `GET /reader-renew-books` - Renew a book

#### Information Endpoints (`/api/`)
- `GET /reader-log-up` - Register new reader
- `GET /reader-information` - Get reader details
- `GET /librarian-director-information` - Get librarian/director details
- `POST /update-reader-information` - Update reader info
- `POST /update-librarian-director-information` - Update librarian/director info

#### Librarian Book Operations (`/api/`)
- `GET /libarian-add-books` - Add new book
- `POST /update-book` - Update book info
- `DELETE /delete-book` - Delete book
- `GET /view-report` - View library reports
- `GET /view-library-logs` - View operation logs

#### Librarian Reader Operations (`/api/`)
- `GET /search-readers` - Search readers
- `GET /add-new-reader` - Add new reader
- `POST /update-reader` - Update reader info
- `DELETE /delete-reader` - Delete reader

#### Director Operations (`/api/`)
- `GET /search-librarian` - Search librarians
- `DELETE /delete-librarian` - Delete librarian
- `GET /all-librarians` - Get all librarians
- `POST /add-new-librarian` - Add new librarian

### Features and Functionality

#### User Management
- Three distinct user roles: Reader, Librarian, Library Director
- Role-based access control
- Registration available for readers only
- Profile management for all user types

#### Reader Features
- Book search (by ID, name, author)
- Book borrowing (20-day loan period)
- Book returning functionality
- Book renewing (once, with 10-day extension)
- Personal borrowing history
- Activity calendar visualization
- Personalized reading reports
- Profile editing

#### Librarian Features
- Add new books to library
- Update book information
- Delete books
- Search and manage readers
- Add new readers
- Update reader information
- Delete readers
- View library reports (overdue, borrowed, returned books)
- Access operation logs
- Profile management

#### Director Features
- All librarian functionalities
- Manage librarians (add, search, delete)
- View all librarians
- Profile management

#### System Features
- Operation audit logging
- Due date management
- Book availability tracking
- Database transaction handling

### Database Schema

#### Tables
1. **book** - Stores book information
   - book_id, book_name, author, publisher, publish_year, location, if_available

2. **borrow_record** - Tracks borrow/return operations
   - record_id, student_id, book_id, borrow_date, due_date, return_date, renew

3. **reader_information** - Stores reader account details
   - reader_id, student_id, name, password, email, phone, department, major

4. **librarian_information** - Stores librarian account details
   - admin_id, name, password, email, phone, department

5. **director_information** - Stores director account details
   - admin_id, name, password, email, phone

6. **operation_log** - Logs system operations
   - date, operation

---

## 图书馆管理系统

这是一个综合性的图书馆管理系统，为读者、图书管理员和图书馆馆长提供不同的界面。系统管理图书借阅、归还、续借、用户账户和图书馆操作。

### 项目结构

#### 根目录
- `library.db` - 系统的主要 SQLite 数据库文件
- `README.md` - 项目文档文件
- `Backend/` - 包含所有后端相关文件
- `Frontend/` - 包含传统的 HTML/CSS/JavaScript 前端文件
- `Vue-Frontend/` - 包含 Vue.js 3 前端文件

#### 后端目录结构
- `main.py` - 主要的 FastAPI 应用程序文件，包含路由和认证逻辑
- `requirements.txt` - Python 依赖包列表
- `create_librarian_table.py` - 初始化数据库中图书管理员表的脚本
- `library.db` - 应用程序使用的后端数据库文件
- `api/` - 包含 API 路由模块的目录
  - `books.py` - 与图书操作相关的 API 接口
  - `information.py` - 用户信息管理的 API 接口
  - `librarianBookOperation.py` - 图书管理员图书操作的 API 接口
  - `librarianReaderOperation.py` - 图书管理员读者操作的 API 接口
  - `director.py` - 图书馆馆长操作的 API 接口
- `venv/` - Python 虚拟环境目录（如果创建）

#### 前端目录结构
- `background-animation.js` - p5.js 背景动画的 JavaScript 文件
- `images/` - 包含图像资源的目录
- `Reader/` - 包含读者特定 HTML 页面的目录
  - `login.html` - 读者登录页面
  - `reader-home.html` - 读者主页
  - `search-results.html` - 读者的图书搜索结果页面
  - `my-borrowings.html` - 读者借阅历史页面
  - `profile-edit.html` - 读者个人资料编辑页面
  - `calendar.html` - 读者活动日历视图
- `Librarian/` - 包含图书管理员特定 HTML 页面的目录
  - `librarian-home.html` - 图书管理员主页
  - `manage-books.html` - 图书管理页面
  - `manage-readers.html` - 读者管理页面
  - `librarian-profile.html` - 图书管理员个人资料页面
  - `librarian-book-detail.html` - 图书管理员的图书详情页面
  - `librarian-reader-detail.html` - 图书管理员的读者详情页面
  - `librarian-report.html` - 图书管理员的图书馆报告页面
- `Library-Director/` - 包含图书馆馆长特定 HTML 页面的目录
  - `director-home.html` - 图书馆馆长主页
  - `director-manage-books.html` - 馆长的图书管理页面
  - `director-manage-readers.html` - 馆长的读者管理页面
  - `director-profile.html` - 馆长个人资料页面
  - `director-book-detail.html` - 馆长的图书详情页面
  - `director-reader-detail.html` - 馆长的读者详情页面
  - `director-report.html` - 馆长的图书馆报告页面

#### Vue 前端目录结构
- `index.html` - Vue 应用程序的主要 HTML 入口文件
- `package.json` - Node.js 包配置文件
- `package-lock.json` - Node.js 依赖管理锁定文件
- `vite.config.js` - Vite 构建配置文件
- `src/` - Vue 应用程序的源代码目录
  - `main.js` - Vue 应用程序的主要 JavaScript 入口文件
  - `App.vue` - 根 Vue 组件
  - `assets/` - 包含静态资源（图像、样式等）的目录
  - `components/` - 包含 Vue 组件文件的目录

### 系统要求

- Python 3.8 或更高版本
- Node.js 16 或更高版本
- npm 包管理器

### 安装与运行

#### 后端安装

1. 进入 Backend 目录：
   ```bash
   cd D:\studying\csc3170\LMS\Backend
   ```

2. 创建虚拟环境（可选但推荐）：
   ```bash
   python -m venv venv
   ```

3. 激活虚拟环境：
   - Windows 系统：
     ```bash
     venv\Scripts\activate
     ```

4. 安装所需 Python 包：
   ```bash
   pip install -r requirements.txt
   ```

5. 启动后端服务器：
   ```bash
   python main.py
   ```
   或直接使用 uvicorn：
   ```bash
   uvicorn main:app --reload --port 8000
   ```

后端服务器将在 `http://127.0.0.1:8000` 启动。API 接口将通过 `http://127.0.0.1:8000/api/` 访问。

#### 前端安装

##### 传统 HTML 前端
传统前端位于 `Frontend` 目录中，无需特殊安装。您可以直接在浏览器中打开 HTML 文件：
- 读者登录：`Frontend/Reader/login.html`
- 图书管理员界面：`Frontend/Librarian/librarian-home.html`
- 馆长界面：`Frontend/Library-Director/director-home.html`

##### Vue.js 前端
1. 进入 Vue-Frontend 目录：
   ```bash
   cd D:\studying\csc3170\LMS\Vue-Frontend
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 启动开发服务器：
   ```bash
   npm run dev
   ```

   Vue 前端将在 `http://localhost:5173` (或另一个可用端口) 上运行。

### 架构设计

#### 前端架构
系统提供两种不同的前端实现：
1. **传统的 HTML/CSS/JavaScript 前端** 位于 `Frontend` 目录
2. **现代化的 Vue.js 3 前端** 位于 `Vue-Frontend` 目录

**传统前端：**
- 为读者、图书管理员和图书馆馆长提供独立的界面
- 使用 p5.js 实现动画背景效果
- 纯 JavaScript 实现，使用 HTML/CSS

**Vue.js 前端：**
- 基于 Vue 3 框架构建
- 使用 Vite 作为构建工具
- 包含 FullCalendar 组件用于日历视图
- 组件化架构

#### 后端架构
- **框架**: FastAPI (Python)
- **数据库**: SQLite3 (位于 `Backend/library.db`)
- **结构**: 多层架构，main.py 处理认证和路由
- **API 组织**: 不同功能模块分离
- **验证**: 使用 Pydantic 模型进行请求/响应验证
- **日志**: 全面的服务器端日志记录

### 技术栈

#### 后端
- **语言**: Python 3.x
- **框架**: FastAPI (0.104.1)
- **服务器**: uvicorn (0.24.0)
- **验证**: Pydantic (2.5.0)
- **数据库**: SQLite3 (内置)
- **多部分数据**: python-multipart (0.0.6)

#### 前端
**传统前端：**
- **动画**: p5.js (1.7.0)
- **语言**: HTML, CSS, JavaScript

**Vue.js 前端：**
- **框架**: Vue.js (3.4.21)
- **构建工具**: Vite (5.2.0)
- **日历**: @fullcalendar/vue3 (6.1.19), @fullcalendar/daygrid (6.1.19)
- **开发工具**: @vitejs/plugin-vue (5.2.4)

### API 接口

#### 认证接口
- `POST /api/login` - 用户认证

#### 健康检查
- `GET /health` - 系统健康状态

#### 图书接口 (`/api/`)
- `GET /search-books` - 按查询条件搜索图书
- `GET /reader-borrowings` - 获取读者借阅历史
- `GET /reader-activity-calendar` - 获取阅读活动日历
- `POST /borrow-book` - 借阅图书
- `GET /reader-reading-report` - 生成阅读报告
- `GET /reader-return-books` - 归还图书
- `GET /reader-renew-books` - 续借图书

#### 信息接口 (`/api/`)
- `GET /reader-log-up` - 注册新读者
- `GET /reader-information` - 获取读者详情
- `GET /librarian-director-information` - 获取图书管理员/馆长详情
- `POST /update-reader-information` - 更新读者信息
- `POST /update-librarian-director-information` - 更新图书管理员/馆长信息

#### 图书管理员图书操作 (`/api/`)
- `GET /libarian-add-books` - 添加新图书
- `POST /update-book` - 更新图书信息
- `DELETE /delete-book` - 删除图书
- `GET /view-report` - 查看图书馆报告
- `GET /view-library-logs` - 查看操作日志

#### 图书管理员读者操作 (`/api/`)
- `GET /search-readers` - 搜索读者
- `GET /add-new-reader` - 添加新读者
- `POST /update-reader` - 更新读者信息
- `DELETE /delete-reader` - 删除读者

#### 馆长操作 (`/api/`)
- `GET /search-librarian` - 搜索图书管理员
- `DELETE /delete-librarian` - 删除图书管理员
- `GET /all-librarians` - 获取所有图书管理员
- `POST /add-new-librarian` - 添加新图书管理员

### 功能特性

#### 用户管理
- 三种不同的用户角色：读者、图书管理员、图书馆馆长
- 基于角色的访问控制
- 仅读者可注册
- 所有用户类型均可管理个人资料

#### 读者功能
- 图书搜索（按 ID、书名、作者）
- 图书借阅（20 天借阅期）
- 图书归还功能
- 图书续借（一次，延长 10 天）
- 个人借阅历史
- 活动日历可视化
- 个性化阅读报告
- 个人资料编辑

#### 图书管理员功能
- 向图书馆添加新书
- 更新图书信息
- 删除图书
- 搜索和管理读者
- 添加新读者
- 更新读者信息
- 删除读者
- 查看图书馆报告（逾期、借出、归还图书）
- 访问操作日志
- 个人资料管理

#### 馆长功能
- 所有图书管理员功能
- 管理图书管理员（添加、搜索、删除）
- 查看所有图书管理员
- 个人资料管理

#### 系统特性
- 操作审计日志
- 到期日管理
- 图书可用性跟踪
- 数据库事务处理

### 数据库结构

#### 表格
1. **book** - 存储图书信息
   - book_id, book_name, author, publisher, publish_year, location, if_available

2. **borrow_record** - 跟踪借阅/归还操作
   - record_id, student_id, book_id, borrow_date, due_date, return_date, renew

3. **reader_information** - 存储读者账户详情
   - reader_id, student_id, name, password, email, phone, department, major

4. **librarian_information** - 存储图书管理员账户详情
   - admin_id, name, password, email, phone, department

5. **director_information** - 存储馆长账户详情
   - admin_id, name, password, email, phone

6. **operation_log** - 记录系统操作
   - date, operation