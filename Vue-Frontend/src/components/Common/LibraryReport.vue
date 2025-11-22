<template>
  <div class="director-report-container">
    <div class="content">
      <button class="back-btn" @click="goBack">&lt; BACK</button>

      <div class="layout">
        <div class="date-selector">
          <h3>Select Date</h3>
          <div class="date-inputs">
            <div class="year-selector">
              <label for="year">Year</label>
              <select id="year" v-model="selectedYear" @change="updateSelectedDate">
                <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
              </select>
            </div>
            
            <div class="month-selector">
              <label for="month">Month</label>
              <select id="month" v-model="selectedMonth" @change="updateSelectedDate">
                <option v-for="month in months" :key="month.value" :value="month.value">{{ month.name }}</option>
              </select>
            </div>
            
            <div class="day-selector">
              <label for="day">Day</label>
              <select id="day" v-model="selectedDay" @change="updateSelectedDate">
                <option v-for="day in daysInMonth" :key="day" :value="day">{{ day }}</option>
              </select>
            </div>
          </div>
        </div>

        <div class="panels">
          <div class="panel">
            <h3>Report · {{ formatDateForTitle(selectedDate) }}</h3>
            <ul v-if="reportData">
              <li>Today's borrowing: {{ reportData['books borrowed today'] || 0 }}</li>
              <li v-if="reportData['books borrowed today detail'] && reportData['books borrowed today detail'].length > 0">
                <details>
                  <summary>Borrowed books details:</summary>
                  <ul style="margin-top: 8px; padding-left: 20px;">
                    <li v-for="(book, index) in reportData['books borrowed today detail']" :key="index"
                        style="padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                      <span style="display: block; font-weight: 500;">{{ book.book_name }} by {{ book.author }}</span>
                      <span style="font-size: 0.9em; color: rgba(255,255,255,0.7);">Student: {{ book.student_id }}, Borrowed: {{ book.borrow_date }}, Due: {{ book.due_date }}</span>
                    </li>
                  </ul>
                </details>
              </li>
              <li>Overdue books: {{ reportData.overdue_books || 0 }}</li>
              <li v-if="reportData['overdue_books detail'] && reportData['overdue_books detail'].length > 0">
                <details>
                  <summary>Overdue books details:</summary>
                  <ul style="margin-top: 8px; padding-left: 20px;">
                    <li v-for="(book, index) in reportData['overdue_books detail']" :key="index"
                        style="padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                      <span style="display: block; font-weight: 500;">{{ book.book_name }} by {{ book.author }}</span>
                      <span style="font-size: 0.9em; color: rgba(255,255,255,0.7);">Student: {{ book.student_id }}, Borrowed: {{ book.borrow_date }}, Due: {{ book.due_date }}</span>
                    </li>
                  </ul>
                </details>
              </li>
              <li>Books didn't return until today: {{ reportData['books didn\'t return until today'] || 0 }}</li>
              <li v-if="reportData['books didn\'t return until today detail'] && reportData['books didn\'t return until today detail'].length > 0">
                <details>
                  <summary>Not returned books details:</summary>
                  <ul style="margin-top: 8px; padding-left: 20px;">
                    <li v-for="(book, index) in reportData['books didn\'t return until today detail']" :key="index"
                        style="padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                      <span style="display: block; font-weight: 500;">{{ book.book_name }} by {{ book.author }}</span>
                      <span style="font-size: 0.9em; color: rgba(255,255,255,0.7);">Student: {{ book.student_id }}, Borrowed: {{ book.borrow_date }}, Due: {{ book.due_date }}</span>
                    </li>
                  </ul>
                </details>
              </li>
              <li>Books returned today: {{ reportData['books returned today'] || 0 }}</li>
              <li v-if="reportData['books returned today detail'] && reportData['books returned today detail'].length > 0">
                <details>
                  <summary>Returned books details:</summary>
                  <ul style="margin-top: 8px; padding-left: 20px;">
                    <li v-for="(book, index) in reportData['books returned today detail']" :key="index"
                        style="padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                      <span style="display: block; font-weight: 500;">{{ book.book_name }} by {{ book.author }}</span>
                      <span style="font-size: 0.9em; color: rgba(255,255,255,0.7);">Student: {{ book.student_id }}, Borrowed: {{ book.borrow_date }}, Returned: {{ book.return_date }}</span>
                    </li>
                  </ul>
                </details>
              </li>
            </ul>
            <ul v-else>
              <li>Loading report data...</li>
            </ul>
          </div>
          <div class="panel">
            <h3>Log · {{ formatDateForTitle(selectedDate) }}</h3>
            <ul v-if="logData">
              <li v-for="(log, index) in logData.logs" :key="index">
                {{ log.operation }} · {{ new Date(log.date).toLocaleTimeString() }}
              </li>
              <li v-if="logData.logs.length === 0">
                No logs for this day
              </li>
            </ul>
            <ul v-else>
              <li>Loading log data...</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LibraryReport',
  props: {
    initialDate: {
      type: Date,
      default: () => new Date()
    }
  },
  data() {
    const date = this.initialDate;
    return {
      selectedDate: new Date(date),
      selectedYear: date.getFullYear(),
      selectedMonth: date.getMonth(), // 0-11
      selectedDay: date.getDate(),
      reportData: null, // 存储报表数据
      logData: null,    // 存储日志数据
      months: [
        { name: 'January', value: 0 },
        { name: 'February', value: 1 },
        { name: 'March', value: 2 },
        { name: 'April', value: 3 },
        { name: 'May', value: 4 },
        { name: 'June', value: 5 },
        { name: 'July', value: 6 },
        { name: 'August', value: 7 },
        { name: 'September', value: 8 },
        { name: 'October', value: 9 },
        { name: 'November', value: 10 },
        { name: 'December', value: 11 }
      ]
    }
  },
  computed: {
    years() {
      const currentYear = new Date().getFullYear();
      const startYear = currentYear - 10;
      const endYear = currentYear + 10;
      const years = [];
      for (let i = startYear; i <= endYear; i++) {
        years.push(i);
      }
      return years;
    },
    daysInMonth() {
      // 计算当前年月的天数
      const date = new Date(this.selectedYear, this.selectedMonth + 1, 0); // 下个月的第0天就是当前月的最后一天
      const days = [];
      for (let i = 1; i <= date.getDate(); i++) {
        days.push(i);
      }
      return days;
    },
    // 格式化日期为YYYY-MM-DD格式，用于API调用
    formattedDate() {
      const year = this.selectedYear;
      const month = String(this.selectedMonth + 1).padStart(2, '0');
      const day = String(this.selectedDay).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  },
  methods: {
    goBack() {
      this.$emit('back');
    },
    updateSelectedDate() {
      // 确保日期有效（例如2月30日）
      const maxDay = new Date(this.selectedYear, this.selectedMonth + 1, 0).getDate();
      if (this.selectedDay > maxDay) {
        this.selectedDay = maxDay;
      }

      this.selectedDate = new Date(this.selectedYear, this.selectedMonth, this.selectedDay);
      // 日期更改后获取新的报告和日志数据
      this.fetchReportData();
      this.fetchLogData();
    },
    formatDateForTitle(date) {
      return `${date.getMonth() + 1}.${date.getDate()}`;
    },
    // 获取报告数据
    async fetchReportData() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/view-report?date=${this.formattedDate}`);
        const data = await response.json();

        if (response.ok) {
          this.reportData = data;
        } else {
          console.error('Failed to fetch report data:', data.detail);
          // 保留原来的数据或显示错误信息
        }
      } catch (error) {
        console.error('Error fetching report data:', error);
      }
    },
    // 获取日志数据
    async fetchLogData() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/view-library-logs?date=${this.formattedDate}`);
        const data = await response.json();

        if (response.ok) {
          this.logData = data;
        } else {
          console.error('Failed to fetch log data:', data.detail);
          // 保留原来的数据或显示错误信息
        }
      } catch (error) {
        console.error('Error fetching log data:', error);
      }
    }
  },
  mounted() {
    // 组件挂载时获取初始数据
    this.fetchReportData();
    this.fetchLogData();
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  overflow-x: hidden;
  position: relative;
  color: white;
}

.director-report-container {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  padding: 40px 48px;
  background: linear-gradient(135deg, #0f111a 0%, #1a1d2b 100%);
  width: 100%;
  height: calc(100vh - 100px);
}

.back-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  cursor: pointer;
  margin-bottom: 30px;
  font-weight: 500;
  transition: background 0.3s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 30px;
}

.date-selector {
  padding: 25px;
  border-radius: 16px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.date-selector h3 {
  color: white;
  margin-bottom: 25px;
  font-weight: 600;
  font-size: 1.2rem;
}

.date-inputs {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.date-inputs > div {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.date-inputs label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  font-weight: 500;
}

.date-inputs select {
  padding: 12px 15px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: #000;
  color: white;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
  padding-right: 35px;
}

.date-inputs select:focus {
  border-color: rgba(208, 230, 187, 1);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
}

.panels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.panel {
  min-height: 360px;
  padding: 25px;
  border-radius: 16px;
  background: rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.panel h3 {
  margin-bottom: 20px;
  letter-spacing: 1px;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
}

.panel ul {
  list-style: none;
  line-height: 1.8;
}

.panel ul li {
  color: rgba(255, 255, 255, 0.9);
  padding: 5px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: color 0.3s;
}

.panel ul li:last-child {
  border-bottom: none;
}

/* Responsive design */
@media (max-width: 900px) {
  .layout {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .content {
    padding: 20px;
  }
  
  .date-selector {
    max-width: 400px;
    margin: 0 auto;
  }
}
</style>