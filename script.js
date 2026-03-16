let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

const categoryNames = {
    design: '设计',
    development: '开发',
    writing: '写作',
    translation: '翻译',
    other: '其他'
};

function init() {
    renderTasks();
    setupEventListeners();
}

function setupEventListeners() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const page = e.target.dataset.page;
            switchPage(page);
        });
    });

    document.getElementById('task-form').addEventListener('submit', handlePublishTask);

    document.getElementById('category-filter').addEventListener('change', renderTasks);
    document.getElementById('status-filter').addEventListener('change', renderTasks);
    document.getElementById('search-input').addEventListener('input', renderTasks);

    document.querySelector('.close').addEventListener('click', closeModal);
    document.getElementById('task-modal').addEventListener('click', (e) => {
        if (e.target.id === 'task-modal') {
            closeModal();
        }
    });
}

function switchPage(page) {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-page="${page}"]`).classList.add('active');

    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    document.getElementById(`${page}-page`).classList.add('active');
}

function renderTasks() {
    const categoryFilter = document.getElementById('category-filter').value;
    const statusFilter = document.getElementById('status-filter').value;
    const searchTerm = document.getElementById('search-input').value.toLowerCase();

    let filteredTasks = tasks.filter(task => {
        const matchCategory = categoryFilter === 'all' || task.category === categoryFilter;
        const matchStatus = statusFilter === 'all' || task.status === statusFilter;
        const matchSearch = task.title.toLowerCase().includes(searchTerm) || 
                           task.description.toLowerCase().includes(searchTerm);
        return matchCategory && matchStatus && matchSearch;
    });

    const taskList = document.getElementById('task-list');

    if (filteredTasks.length === 0) {
        taskList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <div class="empty-state-text">暂无任务</div>
            </div>
        `;
        return;
    }

    taskList.innerHTML = filteredTasks.map(task => `
        <div class="task-card" onclick="showTaskDetail('${task.id}')">
            <div class="task-header">
                <div class="task-title">${escapeHtml(task.title)}</div>
                <div class="task-reward">¥${task.reward}</div>
            </div>
            <div>
                <span class="task-category">${categoryNames[task.category]}</span>
                <span class="task-status ${task.status}">${task.status === 'open' ? '进行中' : '已完成'}</span>
            </div>
            <div class="task-description">${escapeHtml(task.description)}</div>
            <div class="task-footer">
                <span>📅 ${formatDate(task.deadline)}</span>
                <span>👤 ${escapeHtml(task.publisher)}</span>
            </div>
        </div>
    `).join('');
}

function handlePublishTask(e) {
    e.preventDefault();

    const newTask = {
        id: Date.now().toString(),
        title: document.getElementById('task-title').value,
        category: document.getElementById('task-category').value,
        reward: document.getElementById('task-reward').value,
        deadline: document.getElementById('task-deadline').value,
        description: document.getElementById('task-description').value,
        contact: document.getElementById('task-contact').value,
        publisher: '匿名用户',
        status: 'open',
        createdAt: new Date().toISOString()
    };

    tasks.unshift(newTask);
    saveTasks();
    renderTasks();

    document.getElementById('task-form').reset();
    switchPage('home');
    alert('任务发布成功！');
}

function showTaskDetail(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <h3 class="modal-task-title">${escapeHtml(task.title)}</h3>
        <div class="modal-task-info">
            <div class="modal-info-item">
                <span>💰 悬赏金额：</span>
                <strong>¥${task.reward}</strong>
            </div>
            <div class="modal-info-item">
                <span>📂 分类：</span>
                <strong>${categoryNames[task.category]}</strong>
            </div>
            <div class="modal-info-item">
                <span>📅 截止日期：</span>
                <strong>${formatDate(task.deadline)}</strong>
            </div>
            <div class="modal-info-item">
                <span>📊 状态：</span>
                <strong>${task.status === 'open' ? '进行中' : '已完成'}</strong>
            </div>
            <div class="modal-info-item">
                <span>👤 发布者：</span>
                <strong>${escapeHtml(task.publisher)}</strong>
            </div>
        </div>
        <div class="modal-task-description">
            <h4>任务描述：</h4>
            <p>${escapeHtml(task.description)}</p>
        </div>
        <div class="modal-task-contact">
            <h4>联系方式：</h4>
            <p>${escapeHtml(task.contact)}</p>
        </div>
        ${task.status === 'open' ? `
            <button class="submit-btn" onclick="completeTask('${task.id}')">标记为已完成</button>
        ` : ''}
    `;

    document.getElementById('task-modal').classList.add('show');
}

function completeTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.status = 'completed';
        saveTasks();
        renderTasks();
        closeModal();
        alert('任务已标记为完成！');
    }
}

function closeModal() {
    document.getElementById('task-modal').classList.remove('show');
}

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

if (tasks.length === 0) {
    tasks = [
        {
            id: '1',
            title: '设计公司Logo',
            category: 'design',
            reward: 500,
            deadline: '2026-03-15',
            description: '需要为一家科技公司设计一个简洁、现代的Logo，要求体现创新和科技感。需要提供至少3个设计方案供选择。',
            contact: '微信：company_logo',
            publisher: '科技公司',
            status: 'open',
            createdAt: new Date().toISOString()
        },
        {
            id: '2',
            title: '开发小程序商城',
            category: 'development',
            reward: 3000,
            deadline: '2026-04-01',
            description: '需要开发一个微信小程序商城，包含商品展示、购物车、订单管理、支付等功能。需要有完整的前后端开发经验。',
            contact: 'QQ：123456789',
            publisher: '电商公司',
            status: 'open',
            createdAt: new Date().toISOString()
        },
        {
            id: '3',
            title: '翻译技术文档',
            category: 'translation',
            reward: 800,
            deadline: '2026-03-20',
            description: '需要将一份英文技术文档翻译成中文，文档约5000字，要求翻译准确、专业。需要有相关技术背景。',
            contact: '邮箱：translate@example.com',
            publisher: '软件公司',
            status: 'completed',
            createdAt: new Date().toISOString()
        },
        {
            id: '4',
            title: '撰写产品文案',
            category: 'writing',
            reward: 600,
            deadline: '2026-03-25',
            description: '需要为一款新产品撰写宣传文案，包括产品介绍、卖点提炼、广告语等。要求文案有吸引力、有感染力。',
            contact: '微信：product_writer',
            publisher: '品牌公司',
            status: 'open',
            createdAt: new Date().toISOString()
        }
    ];
    saveTasks();
}

init();