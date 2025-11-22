<template>
  <div class="gh-calendar">
    <div class="controls">
      <div class="left">{{ title }}</div>
    </div>

    <div class="months-row" ref="monthsRow">
      <div v-for="month in months" :key="month.key" class="month-col">
        <div class="month-label">{{ month.label }}</div>

        <div
          class="days-grid"
          :style="{
            gridTemplateColumns: `repeat(${month.cols}, var(--cell-size))`,
            width: month.gridWidth
          }"
        >
          <div
            v-for="day in month.days"
            :key="`${month.key}-${day.date}`"
            class="cell"
            :style="getCellActivityStyle(day)"
            @mouseenter="onHoverCell(month, day)"
            @mouseleave="hideTooltip"
            @click="onCellClick(day)"
          >
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="tooltip.show"
      class="tooltip"
      :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
    >
      {{ tooltip.text }}
    </div>

    <!-- Activity level legend -->
    <div class="activity-legend">
      <div class="legend-label">Less</div>
      <div class="legend-colors">
        <div class="legend-color" style="background-color: rgb(0,191,255);"></div>
        <div class="legend-color" style="background-color: rgb(30,144,255);"></div>
        <div class="legend-color" style="background-color: rgb(15, 82, 186);"></div>
      </div>
      <div class="legend-label">More</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReadingCalendar',
  props: {
    monthsToShow: {
      type: Number,
      default: 5
    },
    rowsPerColumn: {
      type: Number,
      default: 7
    },
    title: {
      type: String,
      default: 'Reading Activity'
    }
  },
  data() {
    return {
      months: [],
      tooltip: {
        show: false,
        text: '',
        x: 0,
        y: 0
      },
      metrics: {
        cellSize: 20,
        cellGap: 8
      },
      lastMouse: {
        x: null,
        y: null
      },
      activityData: {}  // Store the activity data from API
    }
  },
  async mounted() {
    this.syncMetrics();
    await this.generateCalendarData();
    await this.loadActivityData();  // Load activity data from backend
    window.addEventListener('mousemove', this.handleMouseMove);
  },
  beforeUnmount() {
    window.removeEventListener('mousemove', this.handleMouseMove);
  },
  methods: {
    syncMetrics() {
      const styles = getComputedStyle(document.documentElement);
      const cellSize = parseInt(styles.getPropertyValue('--cell-size')) || 20;
      const cellGap = parseInt(styles.getPropertyValue('--cell-gap')) || 8;
      this.metrics = { cellSize, cellGap };
    },

    // Helper function to get days in a month
    daysInMonth(year, monthIndex) {
      return new Date(year, monthIndex + 1, 0).getDate();
    },

    // Generate calendar data following the HTML reference
    generateCalendarData() {
      const now = new Date();
      const months = [];
      const totalMonths = this.monthsToRender;
      const rowsPerColumn = this.rowsPerColumnValue;

      for (let i = totalMonths - 1; i >= 0; i--) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const y = d.getFullYear();
        const m = d.getMonth(); // 0..11
        const label = d.toLocaleString('en', { month: 'short' }) + ' ' + y;
        const dayCount = this.daysInMonth(y, m);

        const rows = rowsPerColumn;
        // Columns = ceil(days/rows) => typically 5 or 6
        const cols = Math.ceil(dayCount / rows);

        const days = [];
        for (let day = 1; day <= dayCount; day++) {
          const dateStr = `${y}-${String(m+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
          days.push({ date: dateStr, day });
        }

        months.push({
          key: `${y}-${m}`,
          year: y,
          month: m,
          label,
          days,
          rows,
          cols,
          gridWidth: `${cols * (this.metrics.cellSize + this.metrics.cellGap) + 24}px`
        });
      }

      this.months = months;
      this.scrollToStart();
    },

    // Get the style for a specific day based on activity count
    getCellActivityStyle(day) {
      const activityCount = this.activityData[day.date] || 0;

      if (activityCount === 0) {
        return {
          backgroundColor: 'rgb(192,192,192)',
          border: '1px solid var(--cell-border)'
        };
      } else if (activityCount === 1) {
        return {
          backgroundColor: 'rgb(0, 191, 255)',
          border: '1px solid var(--cell-border)'
        };
      } else if (activityCount >= 2 && activityCount <= 3) {
        return {
          backgroundColor: 'rgb(30, 144, 255)',
          border: '1px solid var(--cell-border)'
        };
      } else if (activityCount > 3) {
        return {
          backgroundColor: 'rgb(15, 82, 186)',
          border: '1px solid var(--cell-border)'
        };
      }

      return {
        backgroundColor: 'rgb(192,192,192)',
        border: '1px solid var(--cell-border)'
      };
    },

    scrollToStart() {
      this.$nextTick(() => {
        const wrap = this.$refs.monthsRow;
        if (wrap) {
          wrap.scrollLeft = 0;
        }
      });
    },

    onHoverCell(month, day) {
      this.tooltip.show = true;
      this.tooltip.text = `${month.label} · Day ${day.day} · ${day.date}`;
      const x = this.lastMouse.x ?? window.innerWidth / 2;
      const y = (this.lastMouse.y ?? window.innerHeight / 2) - 12;
      this.tooltip.x = x;
      this.tooltip.y = y;
    },

    hideTooltip() {
      this.tooltip.show = false;
    },

    onCellClick(day) {
      this.$emit('select-day', day);
    },

    // Load activity data from backend
    async loadActivityData() {
      try {
        // Get student ID from localStorage
        const studentId = localStorage.getItem('userId');

        if (!studentId) {
          console.error('No student ID found');
          return;
        }

        const response = await fetch(`http://127.0.0.1:8000/api/reader-activity-calendar?student_id=${encodeURIComponent(studentId)}`);
        const data = await response.json();

        this.activityData = data.activity_data || {};
      } catch (error) {
        console.error('Error loading activity data:', error);
      }
    },

    handleMouseMove(e) {
      this.lastMouse.x = e.clientX;
      this.lastMouse.y = e.clientY;
      if (this.tooltip.show) {
        this.tooltip.x = e.clientX;
        this.tooltip.y = e.clientY - 12;
      }
    }
  },
  watch: {
    monthsToShow() {
      this.generateCalendarData();
    },
    rowsPerColumn() {
      this.generateCalendarData();
    }
  },
  computed: {
    monthsToRender() {
      return this.monthsToShow || 5;
    },
    rowsPerColumnValue() {
      return this.rowsPerColumn > 0 ? this.rowsPerColumn : 6;
    }
  }
}
</script>

<style scoped>
:global(:root) {
  --calendar-bg: #0b0d0f;
  --calendar-panel: rgba(0, 0, 0, 0.3);
  --calendar-muted: #9aa0a4;
  --cell-border: rgba(255, 255, 255, 0.06);
  --cell-white: #ffffff;
  --cell-empty: rgba(255, 255, 255, 0.02);
  --tooltip-bg: rgba(255, 255, 255, 0.06);
  --tooltip-text: #e8eaec;
  --gap-month: 18px;
  --cell-size: 18px;
  --cell-gap: 6px;
}

.gh-calendar {
  background: var(--calendar-panel);
  padding: 14px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.03);
  position: relative;
  color: #cbd5d8;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.controls .left {
  font-size: 16px;
  color: #e6e9eb;
  font-weight: 600;
}

.controls .right {
  color: var(--calendar-muted);
  font-size: 13px;
}

.months-row {
  display: flex;
  align-items: flex-start;
  gap: var(--gap-month);
  overflow-x: auto;
  padding: 6px 0;
  scroll-behavior: smooth;
}

.month-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}

.month-label {
  font-size: 13px;
  color: var(--calendar-muted);
  margin-bottom: 10px;
  height: 18px;
  text-align: center;
  min-width: 120px;
}

.days-grid {
  display: grid;
  grid-auto-rows: var(--cell-size);
  row-gap: var(--cell-gap);
  column-gap: var(--cell-gap);
  justify-content: center;
  align-items: start;
  padding: 6px;
  border-radius: 8px;
}

.cell {
  width: var(--cell-size);
  height: var(--cell-size);
  border-radius: 6px;
  background: var(--cell-white);
  border: 1px solid var(--cell-border);
  box-sizing: border-box;
  cursor: pointer;
  transition: transform 0.06s ease;
}

.cell:active {
  transform: scale(0.98);
}

.cell.empty {
  background: var(--cell-empty);
  border-style: dashed;
  cursor: default;
}

.tooltip {
  position: fixed;
  padding: 8px 10px;
  border-radius: 6px;
  background: var(--tooltip-bg);
  color: var(--tooltip-text);
  font-size: 13px;
  border: 1px solid rgba(255, 255, 255, 0.04);
  pointer-events: none;
  white-space: nowrap;
  transform: translate(-50%, -120%);
  box-shadow: 0 8px 20px rgba(2, 6, 12, 0.6);
}

.activity-legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
  padding: 0 10px;
}

.legend-label {
  font-size: 12px;
  color: var(--calendar-muted);
  white-space: nowrap;
}

.legend-colors {
  display: flex;
  flex: 1;
  height: 16px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
}

.legend-color {
  flex: 1;
  height: 100%;
}

@media (max-width: 900px) {
  :global(:root) {
    --cell-size: 15px;
    --cell-gap: 5px;
    --gap-month: 14px;
  }
  .month-col {
    min-width: 100px;
  }
  .month-label {
    min-width: 100px;
  }

  .activity-legend {
    gap: 4px;
  }

  .legend-label {
    font-size: 11px;
  }

  .legend-colors {
    height: 14px;
  }
}
</style>