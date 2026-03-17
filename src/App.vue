<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <div class="logo-container">
          <div class="logo-icon">🔍</div>
          <h1 class="logo">万事屋</h1>
        </div>
        <nav class="nav">
          <button 
            class="nav-btn" 
            :class="{ active: currentPage === 'home' }" 
            @click="currentPage = 'home'; fetchTasks()"
          >
            首页
          </button>
          <button 
            class="nav-btn" 
            :class="{ active: currentPage === 'publish' }" 
            @click="checkLogin('publish')"
          >
            发布任务
          </button>
          <button 
            class="nav-btn" 
            v-if="isLoggedIn"
            :class="{ active: currentPage === 'myTasks' }" 
            @click="currentPage = 'myTasks'; fetchMyTasks()"
          >
            已发布任务
          </button>
          <button 
            class="nav-btn" 
            v-if="!isLoggedIn" 
            @click="currentPage = 'login'"
          >
            登录
          </button>
          <button 
            class="nav-btn" 
            v-if="!isLoggedIn" 
            @click="currentPage = 'register'"
          >
            注册
          </button>
          <button 
            class="nav-btn" 
            v-if="isLoggedIn" 
            @click="handleLogout"
          >
            退出
          </button>
          <span v-if="isLoggedIn" class="user-info">
            欢迎, {{ user.username }}
          </span>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <!-- 首页 -->
        <section v-if="currentPage === 'home'" class="page active">
          <div class="home-grid">
            <aside class="sidebar">
              <div class="panel">
                <h3 class="panel-title">筛选条件</h3>
                <div class="panel-body">
                  <label>分类</label>
                  <select v-model="categoryFilter" @change="fetchTasks">
                    <option value="all">所有分类</option>
                    <option v-for="category in categories" :key="category.id" :value="category.name">
                      {{ category.name }}
                    </option>
                    <option value="design">设计</option>
                    <option value="development">开发</option>
                    <option value="writing">写作</option>
                    <option value="translation">翻译</option>
                    <option value="reward">悬赏</option>
                    <option value="game">游戏</option>
                    <option value="trade">交易</option>
                    <option value="charity">公益</option>
                    <option value="other">其他</option>
                  </select>

                  <label class="mt-12">状态</label>
                  <select v-model="activeCategory" @change="fetchTasks">
                    <option value="all">全部</option>
                    <option value="open">进行中</option>
                    <option value="completed">已完成</option>
                  </select>

                  <label class="mt-12">关键字</label>
                  <div class="search-container">
                    <input type="text" v-model="searchTerm" placeholder="搜索任务...">
                    <button class="search-btn" @click="fetchTasks">🔍</button>
                  </div>
                </div>
              </div>

              <div class="panel mt-16">
                <h3 class="panel-title">热门分类</h3>
                <div class="category-tags">
                  <button class="category-tag" :class="{ active: activeCategory=== 'reward'}" @click="activeCategory='reward'">悬赏</button>
                  <button class="category-tag" :class="{ active: activeCategory=== 'game'}" @click="activeCategory='game'">游戏</button>
                  <button class="category-tag" :class="{ active: activeCategory=== 'development'}" @click="activeCategory='development'">开发</button>
                  <button class="category-tag" :class="{ active: activeCategory=== 'charity'}" @click="activeCategory='charity'">公益</button>
                </div>
              </div>
            </aside>

            <section class="main-content">
              <div class="task-list">
                <div
                  v-for="task in getTasksForHome()"
                  :key="task.id"
                  class="task-card"
                  @click="showTaskDetail(task)"
                >
                  <div class="task-header">
                    <div class="task-title">{{ task.title }}</div>
                    <div class="task-reward">¥{{ task.reward }}</div>
                  </div>
                  <div>
                    <span class="task-category">{{ categoryNames[task.category] || task.category }}</span>
                    <span class="task-status" :class="task.status">
                      {{ task.status === 'open' ? '进行中' : '已完成' }}
                    </span>
                  </div>
                  <div class="task-description">{{ task.description }}</div>
                  <div class="task-footer">
                    <span>📅 {{ formatDate(task.deadline) }}</span>
                    <span>👤 {{ task.publisher }}</span>
                    <span v-if="task.assignee" class="task-assignee">✅ {{ task.assignee }}</span>
                  </div>
                </div>

                <div v-if="getTasksForHome().length === 0" class="empty-state">
                  <div class="empty-state-icon">📋</div>
                  <div class="empty-state-text">暂无任务，稍后再来看看</div>
                </div>
              </div>
            </section>

            <aside class="right-panel">
              <div class="panel">
                <h3 class="panel-title">今日热榜</h3>
                <ul class="hot-list">
                  <li v-for="task in getTasksForHome().slice(0, 6)" :key="task.id" @click="showTaskDetail(task)">
                    <span>·</span> {{ task.title }}
                  </li>
                </ul>
              </div>

              <div class="panel mt-16">
                <h3 class="panel-title">统计</h3>
                <div class="stats-list">
                  <div class="stat-item"><strong>{{ tasks.length }}</strong><span>任务总量</span></div>
                  <div class="stat-item"><strong>{{ tasks.filter(t => t.status === 'open').length }}</strong><span>进行中</span></div>
                  <div class="stat-item"><strong>{{ tasks.filter(t => t.status === 'completed').length }}</strong><span>已完成</span></div>
                </div>
              </div>
            </aside>
          </div>
        </section>

        <!-- 发布任务页 -->
        <section v-if="currentPage === 'publish'" class="page">
          <div class="publish-form">
            <h2>发布新任务</h2>
            <form @submit.prevent="handlePublishTask">
              <div class="form-group">
                <label for="task-title">任务标题</label>
                <input 
                  type="text" 
                  id="task-title" 
                  v-model="newTask.title" 
                  required
                >
              </div>
              <div class="form-group">
                <label for="task-category">任务分类</label>
                <select 
                  id="task-category" 
                  v-model="newTask.category" 
                  required
                >
                  <option value="">请选择分类</option>
                  <option v-for="category in categories" :key="category.id" :value="category.name">
                    {{ category.name }}
                  </option>
                  <option value="design">设计</option>
                  <option value="development">开发</option>
                  <option value="writing">写作</option>
                  <option value="translation">翻译</option>
                  <option value="reward">悬赏</option>
                  <option value="game">游戏</option>
                  <option value="trade">交易</option>
                  <option value="charity">公益</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label for="task-reward">悬赏金额 (元)</label>
                <input 
                  type="number" 
                  id="task-reward" 
                  v-model.number="newTask.reward" 
                  min="1" 
                  required
                >
              </div>
              <div class="form-group">
                <label for="task-deadline">截止日期</label>
                <input 
                  type="date" 
                  id="task-deadline" 
                  v-model="newTask.deadline" 
                  required
                >
              </div>
              <div class="form-group">
                <label for="task-description">任务描述</label>
                <textarea 
                  id="task-description" 
                  rows="5" 
                  v-model="newTask.description" 
                  required
                ></textarea>
              </div>
              <div class="form-group">
                <label for="task-contact">联系方式</label>
                <input 
                  type="text" 
                  id="task-contact" 
                  v-model="newTask.contact" 
                  required
                >
              </div>
              <button type="submit" class="submit-btn" :disabled="isLoading">
                {{ isLoading ? '发布中...' : '发布任务' }}
              </button>
            </form>
          </div>
        </section>

        <!-- 登录页 -->
        <section v-if="currentPage === 'login'" class="page">
          <div class="login-form">
            <h2>用户登录</h2>
            <form @submit.prevent="handleLogin">
              <div class="form-group">
                <label for="login-username">用户名</label>
                <input 
                  type="text" 
                  id="login-username" 
                  v-model="loginForm.username" 
                  required
                >
              </div>
              <div class="form-group">
                <label for="login-password">密码</label>
                <input 
                  type="password" 
                  id="login-password" 
                  v-model="loginForm.password" 
                  required
                >
              </div>
              <button type="submit" class="submit-btn" :disabled="isLoading">
                {{ isLoading ? '登录中...' : '登录' }}
              </button>
              <div class="form-footer">
                还没有账号？ <a href="#" @click.prevent="currentPage = 'register'">立即注册</a>
              </div>
            </form>
          </div>
        </section>

        <!-- 已发布任务页 -->
        <section v-if="currentPage === 'myTasks'" class="page active">
          <h2>我的已发布任务</h2>
          <div class="task-list">
            <div 
              v-for="task in myTasks" 
              :key="task.id" 
              class="task-card" 
              @click="showTaskDetail(task)"
            >
              <div class="task-header">
                <div class="task-title">{{ task.title }}</div>
                <div class="task-reward">¥{{ task.reward }}</div>
              </div>
              <div>
                <span class="task-category">{{ categoryNames[task.category] }}</span>
                <span class="task-status" :class="task.status">
                  {{ task.status === 'open' ? '进行中' : '已完成' }}
                </span>
              </div>
              <div class="task-description">{{ task.description }}</div>
              <div class="task-footer">
                <span>📅 {{ formatDate(task.deadline) }}</span>
                <span>👤 {{ task.publisher }}</span>
                <span v-if="task.assignee" class="task-assignee">✅ {{ task.assignee }}</span>
              </div>
            </div>
            <div v-if="myTasks.length === 0" class="empty-state">
              <div class="empty-state-icon">📋</div>
              <div class="empty-state-text">暂无已发布任务</div>
            </div>
          </div>
          
          <!-- 分页控件 -->
          <div class="pagination" v-if="myTotalPages > 1">
            <button 
              class="pagination-btn" 
              @click="changeMyPage(myCurrentPageNum - 1)" 
              :disabled="myCurrentPageNum === 1"
            >
              上一页
            </button>
            
            <span class="pagination-info">
              第 {{ myCurrentPageNum }} 页 / 共 {{ myTotalPages }} 页
            </span>
            
            <button 
              class="pagination-btn" 
              @click="changeMyPage(myCurrentPageNum + 1)" 
              :disabled="myCurrentPageNum === myTotalPages"
            >
              下一页
            </button>
          </div>
        </section>

        <!-- 注册页 -->
        <section v-if="currentPage === 'register'" class="page">
          <div class="register-form">
            <h2>用户注册</h2>
            <form @submit.prevent="handleRegister">
              <div class="form-group">
                <label for="register-username">用户名</label>
                <input 
                  type="text" 
                  id="register-username" 
                  v-model="registerForm.username" 
                  required
                >
              </div>
              <div class="form-group">
                <label for="register-email">邮箱</label>
                <input 
                  type="email" 
                  id="register-email" 
                  v-model="registerForm.email" 
                  required
                >
              </div>
              <div class="form-group">
                <label for="register-password">密码</label>
                <input 
                  type="password" 
                  id="register-password" 
                  v-model="registerForm.password" 
                  required
                >
              </div>
              <button type="submit" class="submit-btn" :disabled="isLoading">
                {{ isLoading ? '注册中...' : '注册' }}
              </button>
              <div class="form-footer">
                已有账号？ <a href="#" @click.prevent="currentPage = 'login'">立即登录</a>
              </div>
            </form>
          </div>
        </section>
      </div>
    </main>

    <!-- 任务详情模态框 -->
    <div 
      id="task-modal" 
      class="modal" 
      :class="{ show: showModal }"
      @click.self="closeModal"
    >
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <div v-if="selectedTask" class="modal-body">
          <h3 class="modal-task-title">{{ selectedTask.title }}</h3>
          <div class="modal-task-info">
            <div class="modal-info-item">
              <span>💰 悬赏金额：</span>
              <strong>¥{{ selectedTask.reward }}</strong>
            </div>
            <div class="modal-info-item">
              <span>📂 分类：</span>
              <strong>{{ categoryNames[selectedTask.category] }}</strong>
            </div>
            <div class="modal-info-item">
              <span>📅 截止日期：</span>
              <strong>{{ formatDate(selectedTask.deadline) }}</strong>
            </div>
            <div class="modal-info-item">
              <span>📊 状态：</span>
              <strong>{{ selectedTask.status === 'open' ? '进行中' : '已完成' }}</strong>
            </div>
            <div class="modal-info-item">
              <span>👤 发布者：</span>
              <strong>{{ selectedTask.publisher }}</strong>
            </div>
            <div class="modal-info-item" v-if="selectedTask.assignee">
              <span>✅ 接受者：</span>
              <strong>{{ selectedTask.assignee }}</strong>
            </div>
          </div>
          <div class="modal-task-description">
            <h4>任务描述：</h4>
            <p>{{ selectedTask.description }}</p>
          </div>
          <div class="modal-task-contact">
            <h4>联系方式：</h4>
            <p>{{ selectedTask.contact }}</p>
          </div>
          <button 
            v-if="selectedTask.status === 'open' && isLoggedIn && selectedTask.publisher === user.username" 
            class="submit-btn" 
            @click="completeTask(selectedTask.id)"
            :disabled="isLoading"
          >
            {{ isLoading ? '处理中...' : '标记为已完成' }}
          </button>
          <button 
            v-else-if="selectedTask.status === 'open' && isLoggedIn && !selectedTask.assignee && selectedTask.publisher !== user.username" 
            class="submit-btn" 
            @click="acceptTask(selectedTask.id)"
            :disabled="isLoading"
          >
            {{ isLoading ? '处理中...' : '接受任务' }}
          </button>
          <div v-else-if="selectedTask.status === 'open' && isLoggedIn && selectedTask.assignee" class="login-tip">
            该任务已被其他用户接受
          </div>
          <div v-else-if="selectedTask.status === 'open' && isLoggedIn" class="login-tip">
            只有任务的发布者才能标记任务为已完成
          </div>
          <div v-if="!isLoggedIn" class="login-tip">
            请先登录后操作
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      currentPage: 'home',
      tasks: [],
      newTask: {
        title: '',
        category: '',
        reward: 0,
        deadline: '',
        description: '',
        contact: ''
      },
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        email: '',
        password: ''
      },
      categoryFilter: 'all',
      statusFilter: 'all',
      searchTerm: '',
      activeCategory: 'all',
      showModal: false,
      selectedTask: null,
      isLoading: false,
      isLoggedIn: false,
      user: {},
      token: null,
      categories: [],
      categoryNames: {
        design: '设计',
        development: '开发',
        writing: '写作',
        translation: '翻译',
        reward: '悬赏',
        game: '游戏',
        trade: '交易',
        charity: '公益',
        other: '其他'
      },
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api',
      // 分页相关
      currentPageNum: 1,
      totalPages: 1,
      totalTasks: 0,
      // 已发布任务相关
      myTasks: [],
      myCurrentPageNum: 1,
      myTotalPages: 1,
      myTotalTasks: 0
    }
  },
  mounted() {
    this.checkAuth();
    this.fetchCategories();
    this.fetchTasks();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      if (token && user) {
        this.token = token;
        this.user = JSON.parse(user);
        this.isLoggedIn = true;
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/categories/`);
        this.categories = response.data.results;
        // 更新categoryNames
        this.categories.forEach(category => {
          this.categoryNames[category.name] = category.name;
        });
      } catch (error) {
        console.error('获取分类失败:', error);
      }
    },
    async fetchTasks() {
      try {
        this.isLoading = true;
        let url = `${this.apiBaseUrl}/tasks/`;
        
        // 构建查询参数
        const params = {
          status: 'open' // 只获取进行中的任务
        };
        // 只有在非首页时才使用分页和分类过滤
        if (this.currentPage !== 'home') {
          params.page = this.currentPageNum;
          if (this.categoryFilter !== 'all') {
            params.category = this.categoryFilter;
          }
        } else {
          // 首页获取更多任务，确保所有分类都有数据显示
          params.page_size = 100;
        }
        if (this.searchTerm) {
          params.search = this.searchTerm;
        }
        
        // 添加查询参数到 URL
        url += '?' + new URLSearchParams(params).toString();
        
        const config = this.token ? { headers: { Authorization: `Bearer ${this.token}` } } : {};
        const response = await axios.get(url, config);
        this.tasks = response.data.results;
        this.totalTasks = response.data.count;
        this.totalPages = Math.ceil(this.totalTasks / 10); // 每页10条
      } catch (error) {
        console.error('获取任务失败:', error);
        alert('获取任务失败，请稍后重试');
      } finally {
        this.isLoading = false;
      }
    },
    async handlePublishTask() {
      try {
        this.isLoading = true;
        const taskData = {
          ...this.newTask,
          publisher: this.user.username,
          status: 'open'
        };
        
        const response = await axios.post(`${this.apiBaseUrl}/tasks/`, taskData, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        });
        
        this.newTask = {
          title: '',
          category: '',
          reward: 0,
          deadline: '',
          description: '',
          contact: ''
        };
        
        this.currentPage = 'home';
        this.fetchTasks();
        alert('任务发布成功！');
      } catch (error) {
        console.error('发布任务失败:', error);
        alert('发布任务失败，请稍后重试');
      } finally {
        this.isLoading = false;
      }
    },
    async handleLogin() {
      try {
        this.isLoading = true;
        const response = await axios.post(`${this.apiBaseUrl}/auth/login/`, this.loginForm);
        
        const { access, ...userData } = response.data;
        
        localStorage.setItem('token', access);
        localStorage.setItem('user', JSON.stringify(userData));
        
        this.token = access;
        this.user = userData;
        this.isLoggedIn = true;
        
        this.loginForm = {
          username: '',
          password: ''
        };
        
        this.currentPage = 'home';
        alert('登录成功！');
      } catch (error) {
        console.error('登录失败:', error);
        alert('登录失败，请检查用户名和密码');
      } finally {
        this.isLoading = false;
      }
    },
    async handleRegister() {
      try {
        this.isLoading = true;
        const response = await axios.post(`${this.apiBaseUrl}/auth/register/`, this.registerForm);
        
        const { access, ...userData } = response.data;
        
        localStorage.setItem('token', access);
        localStorage.setItem('user', JSON.stringify(userData));
        
        this.token = access;
        this.user = userData;
        this.isLoggedIn = true;
        
        this.registerForm = {
          username: '',
          email: '',
          password: ''
        };
        
        this.currentPage = 'home';
        alert('注册成功！');
      } catch (error) {
        console.error('注册失败:', error);
        alert('注册失败，请检查输入信息');
      } finally {
        this.isLoading = false;
      }
    },
    handleLogout() {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      this.token = null;
      this.user = {};
      this.isLoggedIn = false;
      this.currentPage = 'home';
      alert('已退出登录');
    },
    checkLogin(page) {
      if (this.isLoggedIn) {
        this.currentPage = page;
      } else {
        this.currentPage = 'login';
        alert('请先登录');
      }
    },
    showTaskDetail(task) {
      this.selectedTask = task;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedTask = null;
    },
    async completeTask(taskId) {
      try {
        // 检查当前用户是否是任务的发布者
        const task = this.tasks.find(t => t.id === taskId) || this.myTasks.find(t => t.id === taskId);
        if (!task) {
          alert('任务不存在');
          return;
        }
        
        if (task.publisher !== this.user.username) {
          alert('只有任务的发布者才能标记任务为已完成');
          return;
        }
        
        this.isLoading = true;
        await axios.patch(`${this.apiBaseUrl}/tasks/${taskId}/`, {
          status: 'completed'
        }, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        });
        
        this.closeModal();
        this.fetchTasks();
        if (this.currentPage === 'myTasks') {
          this.fetchMyTasks();
        }
        alert('任务已标记为完成！');
      } catch (error) {
        console.error('更新任务状态失败:', error);
        alert('更新任务状态失败，请稍后重试');
      } finally {
        this.isLoading = false;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPageNum = page;
        this.fetchTasks();
      }
    },
    async fetchMyTasks() {
      try {
        this.isLoading = true;
        let url = `${this.apiBaseUrl}/tasks/`;
        
        // 构建查询参数
        const params = {
          page: this.myCurrentPageNum,
          publisher: this.user.username,
          status: 'open' // 只获取进行中的任务
        };
        
        // 添加查询参数到 URL
        url += '?' + new URLSearchParams(params).toString();
        
        const config = { headers: { Authorization: `Bearer ${this.token}` } };
        const response = await axios.get(url, config);
        this.myTasks = response.data.results;
        this.myTotalTasks = response.data.count;
        this.myTotalPages = Math.ceil(this.myTotalTasks / 10); // 每页10条
      } catch (error) {
        console.error('获取已发布任务失败:', error);
        alert('获取已发布任务失败，请稍后重试');
      } finally {
        this.isLoading = false;
      }
    },
    changeMyPage(page) {
      if (page >= 1 && page <= this.myTotalPages) {
        this.myCurrentPageNum = page;
        this.fetchMyTasks();
      }
    },
    async acceptTask(taskId) {
      try {
        // 检查当前用户是否是任务的发布者
        const task = this.tasks.find(t => t.id === taskId) || this.myTasks.find(t => t.id === taskId);
        if (!task) {
          alert('任务不存在');
          return;
        }
        
        if (task.publisher === this.user.username) {
          alert('不能接受自己发布的任务');
          return;
        }
        
        if (task.assignee) {
          alert('该任务已被其他用户接受');
          return;
        }
        
        this.isLoading = true;
        await axios.patch(`${this.apiBaseUrl}/tasks/${taskId}/`, {
          assignee: this.user.username
        }, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        });
        
        this.closeModal();
        this.fetchTasks();
        if (this.currentPage === 'myTasks') {
          this.fetchMyTasks();
        }
        alert('任务接受成功！');
      } catch (error) {
        console.error('接受任务失败:', error);
        alert('接受任务失败，请稍后重试');
      } finally {
        this.isLoading = false;
      }
    },
    getTasksForHome() {
      let list = Array.isArray(this.tasks) ? this.tasks : [];

      if (this.activeCategory !== 'all') {
        list = list.filter(task => task.category === this.activeCategory);
      }

      if (this.searchTerm) {
        const keyword = this.searchTerm.toLowerCase();
        list = list.filter(task =>
          task.title.toLowerCase().includes(keyword) ||
          task.description.toLowerCase().includes(keyword) ||
          task.publisher.toLowerCase().includes(keyword)
        );
      }

      return list;
    },
    getTasksByCategory(category) {
      return this.tasks.filter(task => task.category === category).slice(0, 10);
    }
  }
}
</script>

<style>
/* 全局样式已在 style.css 中定义 */
.login-form,
.register-form {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    margin: 0 auto;
}

.login-form h2,
.register-form h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.form-footer {
    margin-top: 20px;
    text-align: center;
    color: #666;
}

.form-footer a {
    color: #667eea;
    text-decoration: none;
}

.form-footer a:hover {
    text-decoration: underline;
}

.user-info {
    margin-left: 15px;
    color: white;
    font-weight: bold;
}

.login-tip {
    text-align: center;
    margin-top: 20px;
    color: #666;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 5px;
}

/* 分页样式 */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    gap: 15px;
}

.pagination-btn {
    padding: 8px 16px;
    background: #e74c3c;
    color: white;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
}

.pagination-btn:hover:not(:disabled) {
    background: #c0392b;
    transform: translateY(-2px);
}

.pagination-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.pagination-info {
    font-size: 14px;
    color: #666;
}

/* 任务接受者样式 */
.task-assignee {
    margin-left: 10px;
    color: #4CAF50;
    font-weight: bold;
    font-size: 14px;
}

/* 万事屋样式 */
.app {
    background: #f8f9fa;
    min-height: 100vh;
    color: #333;
  }

  .header {
    background: url('https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=minimalist%20abstract%20background%20with%20soft%20colors%20for%20website%20header&image_size=landscape_16_9') center/cover no-repeat;
    padding: 60px 0 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
  }

  .logo-icon {
    font-size: 2rem;
    color: #333;
  }

  .logo {
    font-size: 2rem;
    font-weight: bold;
    margin: 0;
    font-family: 'Arial', 'Microsoft YaHei', sans-serif;
    letter-spacing: 2px;
    color: #333;
  }

  .nav {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
  }

  .nav-btn {
    padding: 8px 16px;
    background: white;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 14px;
  }

  .nav-btn:hover {
    background: #f0f0f0;
    transform: translateY(-2px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .nav-btn.active {
    background: #333;
    color: white;
    border-color: #333;
  }

.task-card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    color: #333;
    border: 1px solid #f0f0f0;
}

.task-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.submit-btn {
    padding: 10px 20px;
    background: #333;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
    margin-top: 15px;
}

.submit-btn:hover:not(:disabled) {
    background: #555;
    transform: translateY(-2px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.submit-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.modal-content {
    background: white;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    color: #333;
}

.filter-bar {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.filter-bar select {
    padding: 8px 16px;
    border: none;
    border-radius: 20px;
    margin-right: 10px;
    font-size: 14px;
    background: rgba(255, 255, 255, 0.9);
  }

  .search-container {
    position: relative;
    display: inline-flex;
    align-items: center;
  }

  .search-container input {
    padding: 8px 40px 8px 16px;
    border: none;
    border-radius: 20px;
    font-size: 14px;
    background: rgba(255, 255, 255, 0.9);
    width: 200px;
  }

  .search-btn {
    position: absolute;
    right: 5px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    font-size: 16px;
    cursor: pointer;
    padding: 5px;
    border-radius: 50%;
    transition: background 0.3s;
  }

  .search-btn:hover {
    background: rgba(192, 57, 43, 0.1);
  }

.empty-state {
    text-align: center;
    padding: 40px 20px;
    background: white;
    border-radius: 10px;
    color: #666;
    border: 1px dashed #ddd;
}

.login-form,
.register-form,
.publish-form {
    background: rgba(255, 255, 255, 0.95);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    max-width: 450px;
    margin: 40px auto;
    color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
    padding: 12px 16px;
    border: 1px solid #ddd;
    border-radius: 25px;
    font-size: 14px;
    width: 100%;
    margin-top: 5px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #333;
}

.user-info {
    margin-left: 15px;
    color: black;
    font-weight: bold;
    background: rgba(192, 57, 43, 0.1);
    border: 1px solid black;
    padding: 5px 15px;
    border-radius: 20px;
  }

  /* 分类水平布局 */
  .categories-grid {
    display: flex;
    gap: 20px;
    margin-top: 30px;
    overflow-x: auto;
    padding-bottom: 20px;
  }

  .categories-grid::-webkit-scrollbar {
    height: 8px;
  }

  .categories-grid::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
  }

  .categories-grid::-webkit-scrollbar-thumb {
    background: rgba(192, 57, 43, 0.5);
    border-radius: 10px;
  }

  .categories-grid::-webkit-scrollbar-thumb:hover {
    background: rgba(192, 57, 43, 0.8);
  }

  .category-column {
    background: white;
    border-radius: 10px;
    padding: 15px;
    min-height: 400px;
    flex: 1;
    min-width: 200px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 1px solid #f0f0f0;
  }

  .category-header {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 15px;
    text-align: center;
    border-bottom: 1px solid #e9ecef;
  }

  .category-header h3 {
    margin: 0;
    color: #333;
    font-size: 16px;
    font-weight: bold;
  }

  .category-tasks {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .category-tasks .task-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
  }

  .category-tasks .task-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .category-tasks .task-title {
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 8px;
  }

  .category-tasks .task-reward {
    font-size: 16px;
    font-weight: bold;
    color: #e74c3c;
  }

  .category-tasks .task-description {
    font-size: 13px;
    line-height: 1.4;
    margin: 10px 0;
    color: #666;
  }

  .category-tasks .task-footer {
    font-size: 12px;
    color: #888;
    margin-top: 10px;
  }

  .category-tasks .empty-state {
    text-align: center;
    padding: 40px 20px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: #fff;
  }
</style>