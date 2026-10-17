
const STORAGE_KEYS = { tasks: 'bloomie.tasks.v1', notes: 'bloomie.notes.v1' };

class TaskItem {
  constructor({ id = crypto.randomUUID(), title, course = 'Umum', dueDate = '', completed = false, createdAt = new Date().toISOString() }) {
    Object.assign(this, { id, title, course: course || 'Umum', dueDate, completed, createdAt });
  }
}

class DashboardApp {
  constructor() {
    this.tasks = this.readStorage(STORAGE_KEYS.tasks, []).map(task => new TaskItem(task));
    this.notes = this.readStorage(STORAGE_KEYS.notes, []);
    this.currentFilter = 'all';
    this.apiTodo = null;

    this.elements = Object.fromEntries([
      'taskForm', 'taskTitle', 'taskCourse', 'taskDue', 'taskList', 'emptyTasks',
      'noteForm', 'noteText', 'notesList', 'emptyNotes', 'noteCharCount',
      'apiStatus', 'totalTasks', 'pendingTasks', 'completedTasks', 'taskCountPill'
    ].map(id => [id, document.querySelector(`#${id}`)]));

    this.bindEvents();
    this.render();
    this.loadExternalData();
  }

  readStorage(key, fallback) {
    try {
      const stored = localStorage.getItem(key);
      return stored ? JSON.parse(stored) : fallback;
    } catch (error) {
      console.warn(`Tidak dapat membaca ${key} dari localStorage.`, error);
      return fallback;
    }
  }

  saveStorage() {
    try {
      localStorage.setItem(STORAGE_KEYS.tasks, JSON.stringify(this.tasks));
      localStorage.setItem(STORAGE_KEYS.notes, JSON.stringify(this.notes));
    } catch (error) {
      if (this.elements.apiStatus) {
        this.elements.apiStatus.textContent = 'Data gagal disimpan. Penyimpanan browser mungkin penuh atau tidak tersedia.';
      }
      console.error('Gagal menyimpan data lokal:', error);
    }
  }

  bindEvents() {
    const e = this.elements;
    const { taskForm, taskTitle, taskCourse, taskDue, taskList, noteForm, noteText, noteCharCount, notesList } = e;

    if (taskForm && taskTitle && taskCourse && taskDue) {
      taskForm.addEventListener('submit', event => {
        event.preventDefault();
        const title = taskTitle.value.trim();
        if (!title) return;

        this.tasks = [...this.tasks, new TaskItem({
          title, course: taskCourse.value.trim() || 'Umum', dueDate: taskDue.value
        })];

        this.saveStorage();
        this.render();
        taskForm.reset();
        taskTitle.focus();
      });
    }

    if (taskList) {
      taskList.addEventListener('change', event => {
        if (!event.target.matches('[data-action="toggle"]')) return;
        const { id } = event.target.dataset;

        this.tasks = this.tasks.map(task => task.id === id
          ? { ...task, completed: event.target.checked }
          : task
        );

        this.saveStorage();
        this.render();
      });

      taskList.addEventListener('click', event => {
        const button = event.target.closest('[data-action]');
        if (!button) return;
        const { action, id } = button.dataset;

        if (action === 'delete') {
          this.tasks = this.tasks.filter(task => task.id !== id);
          this.saveStorage();
          this.render();
        }

        if (action === 'edit') this.editTask(id);
      });
    }

    document.querySelectorAll('[data-filter]').forEach(button => {
      button.addEventListener('click', () => {
        this.currentFilter = button.dataset.filter;
        document.querySelectorAll('[data-filter]').forEach(item =>
          item.classList.toggle('active', item === button)
        );
        this.renderTasks();
      });
    });

    if (noteText && noteCharCount) {
      noteText.addEventListener('input', () => {
        noteCharCount.textContent = `${noteText.value.length}/500`;
      });
    }

    if (noteForm && noteText) {
      noteForm.addEventListener('submit', event => {
        event.preventDefault();
        const text = noteText.value.trim();
        if (!text) return;

        if (text.length > 500) {
          window.alert('Catatan maksimal 500 karakter.');
          return;
        }

        this.notes = [{
          id: crypto.randomUUID(), text, createdAt: new Date().toISOString()
        }, ...this.notes];

        this.saveStorage();
        this.renderNotes();
        noteForm.reset();
        if (noteCharCount) noteCharCount.textContent = '0/500';
      });
    }

    if (notesList) {
      notesList.addEventListener('click', event => {
        const button = event.target.closest('[data-delete-note]');
        if (!button) return;

        this.notes = this.notes.filter(note => note.id !== button.dataset.deleteNote);
        this.saveStorage();
        this.renderNotes();
      });
    }

    const loadSampleButton = document.querySelector('#loadSampleTasks');
    if (loadSampleButton) {
      loadSampleButton.addEventListener('click', () => this.loadSampleTasks());
    }

    const refreshButton = document.querySelector('#refreshButton');
    if (refreshButton) {
      refreshButton.addEventListener('click', () => this.loadExternalData());
    }

    const addApiTodoButton = document.querySelector('#addApiTodo');
    if (addApiTodoButton) {
      addApiTodoButton.addEventListener('click', () => this.addApiTodo());
    }
  }

  editTask(id) {
    const task = this.tasks.find(item => item.id === id);
    if (!task) return;

    const updatedTitle = window.prompt('Edit nama tugas:', task.title);
    if (updatedTitle === null) return;

    const title = updatedTitle.trim();
    if (!title) {
      window.alert('Nama tugas tidak boleh kosong.');
      return;
    }

    const updatedCourse = window.prompt('Edit mata kuliah:', task.course);
    if (updatedCourse === null) return;

    this.tasks = this.tasks.map(item => item.id === id
      ? { ...item, title, course: updatedCourse.trim() || 'Umum' }
      : item
    );

    this.saveStorage();
    this.render();
  }

  loadSampleTasks() {
    const samples = [
      new TaskItem({ title: 'Menyelesaikan laporan praktikum', course: 'Pemrograman Web', dueDate: this.dateOffset(2) }),
      new TaskItem({ title: 'Review materi sebelum kuis', course: 'Jaringan Komputer', dueDate: this.dateOffset(1) }),
      new TaskItem({ title: 'Diskusi kelompok untuk proyek', course: 'Rekayasa Perangkat Lunak', dueDate: this.dateOffset(4) })
    ];

    const existingTitles = new Set(this.tasks.map(task => task.title.toLowerCase()));
    this.tasks = [...this.tasks, ...samples.filter(task => !existingTitles.has(task.title.toLowerCase()))];

    this.saveStorage();
    this.render();
  }

  dateOffset(days) {
    const date = new Date();
    date.setDate(date.getDate() + days);
    return [date.getFullYear(), String(date.getMonth() + 1).padStart(2, '0'), String(date.getDate()).padStart(2, '0')].join('-');
  }

  formatDate(dateString) {
    if (!dateString) return 'Tanpa tenggat';
    const date = new Date(`${dateString}T00:00:00`);
    if (Number.isNaN(date.getTime())) return 'Tanggal tidak valid';

    return new Intl.DateTimeFormat('id-ID', {
      day: 'numeric', month: 'short', year: 'numeric'
    }).format(date);
  }

  formatDateTime(dateString) {
    const date = new Date(dateString);
    if (Number.isNaN(date.getTime())) return 'Waktu tidak tersedia';

    return new Intl.DateTimeFormat('id-ID', {
      day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
    }).format(date);
  }

  render() {
    this.renderTasks();
    this.renderNotes();

    const e = this.elements;
    if (e.totalTasks) e.totalTasks.textContent = this.tasks.length;
    if (e.pendingTasks) e.pendingTasks.textContent = this.tasks.filter(task => !task.completed).length;
    if (e.completedTasks) e.completedTasks.textContent = this.tasks.filter(task => task.completed).length;
    if (e.taskCountPill) e.taskCountPill.textContent = `${this.tasks.length} tugas`;
  }

  renderTasks() {
    const { taskList, emptyTasks } = this.elements;
    if (!taskList || !emptyTasks) return;

    const filteredTasks = this.tasks.filter(task => {
      if (this.currentFilter === 'pending') return !task.completed;
      if (this.currentFilter === 'completed') return task.completed;
      return true;
    });

    taskList.innerHTML = filteredTasks.map(task => `
      <article class="task-item ${task.completed ? 'done' : ''}">
        <input class="task-check" type="checkbox" data-action="toggle"
          data-id="${this.escapeHTML(task.id)}" ${task.completed ? 'checked' : ''}
          aria-label="Tandai ${this.escapeHTML(task.title)} selesai">

        <div class="task-info">
          <div class="task-title">${this.escapeHTML(task.title)}</div>
          <div class="task-meta">
            <span class="course-tag">${this.escapeHTML(task.course)}</span>
            <span>◷ ${this.formatDate(task.dueDate)}</span>
          </div>
        </div>

        <div class="task-actions">
          <button class="small-action" type="button" data-action="edit"
            data-id="${this.escapeHTML(task.id)}" aria-label="Edit tugas">✎</button>
          <button class="small-action" type="button" data-action="delete"
            data-id="${this.escapeHTML(task.id)}" aria-label="Hapus tugas">×</button>
        </div>
      </article>
    `).join('');

    emptyTasks.hidden = filteredTasks.length > 0;
    emptyTasks.textContent = filteredTasks.length === 0 && this.tasks.length > 0
      ? 'Tidak ada tugas untuk filter ini.'
      : 'Belum ada tugas';
  }

  renderNotes() {
    const { notesList, emptyNotes } = this.elements;
    if (!notesList || !emptyNotes) return;

    notesList.innerHTML = this.notes.map(note => `
      <article class="note-item">
        <p>${this.escapeHTML(note.text)}</p>
        <div class="note-item-bottom">
          <span>${this.formatDateTime(note.createdAt)}</span>
          <button type="button" data-delete-note="${this.escapeHTML(note.id)}">Hapus catatan ×</button>
        </div>
      </article>
    `).join('');

    emptyNotes.hidden = this.notes.length > 0;
  }

  escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[character]);
  }

  async loadExternalData() {
    if (this.elements.apiStatus) {
      this.elements.apiStatus.textContent = 'Memuat data dari Open-Meteo, DummyJSON, dan JSONPlaceholder…';
    }

    const results = await Promise.allSettled([
      this.loadWeather(), this.loadQuote(), this.loadApiTodo()
    ]);

    const successes = results.filter(result => result.status === 'fulfilled').length;

    if (this.elements.apiStatus) {
      this.elements.apiStatus.textContent = successes === 3
        ? 'Semua API berhasil dimuat. Data tugas dan catatan tersimpan secara lokal.'
        : `${successes} dari 3 API berhasil dimuat. Periksa koneksi internet, lalu tekan tombol ↻ untuk mencoba lagi.`;
    }

    results.forEach(result => {
      if (result.status === 'rejected') console.error('Gagal memuat data API:', result.reason);
    });
  }

  async loadWeather() {
    const endpoint = 'https://api.open-meteo.com/v1/forecast?latitude=-5.36&longitude=105.31&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=Asia%2FJakarta';
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error('Gagal mengambil cuaca');

    const data = await response.json();
    const current = data.current;
    if (!current) throw new Error('Data cuaca tidak tersedia');

    const description = this.weatherDescription(current.weather_code);
    const setText = (selector, value) => {
      const element = document.querySelector(selector);
      if (element) element.textContent = value;
    };

    setText('#weatherTemp', `${Math.round(current.temperature_2m)}°`);
    setText('#weatherEmoji', this.weatherEmoji(current.weather_code));
    setText('#weatherDesc', description);
    setText('#weatherDetail', `${description}. Terasa seperti ${Math.round(current.apparent_temperature)}°C dengan kelembapan ${current.relative_humidity_2m}%.`);
    setText('#weatherUpdated', `Suhu ${current.temperature_2m}°C · Angin ${current.wind_speed_10m} km/jam`);
  }

  weatherDescription(code) {
    if (code === 0) return 'Cerah';
    if ([1, 2].includes(code)) return 'Cerah berawan';
    if (code === 3) return 'Berawan';
    if ([45, 48].includes(code)) return 'Berkabut';
    if ([51, 53, 55, 56, 57].includes(code)) return 'Gerimis';
    if ([61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return 'Hujan';
    if ([71, 73, 75, 77, 85, 86].includes(code)) return 'Salju';
    if ([95, 96, 99].includes(code)) return 'Badai petir';
    return 'Kondisi cuaca terkini';
  }

  weatherEmoji(code) {
    if (code === 0) return '☀️';
    if ([1, 2, 3].includes(code)) return '⛅';
    if ([45, 48].includes(code)) return '🌫️';
    if ([51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return '🌧️';
    if ([95, 96, 99].includes(code)) return '⛈️';
    return '🌤️';
  }

  async loadQuote() {
    const response = await fetch('https://dummyjson.com/quotes/random');
    if (!response.ok) throw new Error('Gagal mengambil kutipan');

    const data = await response.json();
    const setText = (selector, value) => {
      const element = document.querySelector(selector);
      if (element) element.textContent = value;
    };

    setText('#quoteText', data.quote);
    setText('#quoteAuthor', `— ${data.author}`);
    setText('#quoteDetail', data.quote);
    setText('#quoteDetailAuthor', `— ${data.author}`);
  }

  async loadApiTodo() {
    const response = await fetch('https://jsonplaceholder.typicode.com/todos?_limit=5');
    if (!response.ok) throw new Error('Gagal mengambil contoh tugas');

    const todos = await response.json();
    this.apiTodo = todos.find(todo => !todo.completed) || todos[0] || null;

    const todoText = document.querySelector('#apiTodoText');
    const todoStatus = document.querySelector('#apiTodoStatus');
    if (!this.apiTodo) throw new Error('Contoh tugas tidak tersedia');

    if (todoText) todoText.textContent = this.apiTodo.title;
    if (todoStatus) todoStatus.textContent = `Contoh #${this.apiTodo.id} dari JSONPlaceholder · hanya inspirasi`;
  }

  addApiTodo() {
    if (!this.apiTodo) {
      window.alert('Contoh tugas belum tersedia. Coba muat ulang informasi.');
      return;
    }

    const title = this.apiTodo.title.charAt(0).toUpperCase() + this.apiTodo.title.slice(1);
    this.tasks = [...this.tasks, new TaskItem({ title, course: 'Inspirasi API' })];

    this.saveStorage();
    this.render();
    window.alert('Contoh tugas berhasil ditambahkan ke daftar tugasmu.');
  }
}

const app = new DashboardApp();
