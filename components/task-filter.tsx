import React, { useState } from 'react';

interface TaskFilterProps {
  onFilterChange: (filters: FilterState) => void;
  categories: string[];
  difficulties: string[];
}

interface FilterState {
  search: string;
  category: string;
  difficulty: string;
  sortBy: string;
}

export default function TaskFilter({ onFilterChange, categories, difficulties }: TaskFilterProps) {
  const [filters, setFilters] = useState<FilterState>({
    search: '',
    category: 'all',
    difficulty: 'all',
    sortBy: 'name'
  });

  const handleFilterChange = (key: keyof FilterState, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="task-filter">
      <div className="filter-section">
        <div className="filter-group">
          <label htmlFor="search" className="filter-label">Search Tasks</label>
          <input
            id="search"
            type="text"
            placeholder="Search by title, description, or tags..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="filter-input"
          />
        </div>

        <div className="filter-group">
          <label htmlFor="category" className="filter-label">Category</label>
          <select
            id="category"
            value={filters.category}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            className="filter-select"
          >
            <option value="all">All Categories</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="difficulty" className="filter-label">Difficulty</label>
          <select
            id="difficulty"
            value={filters.difficulty}
            onChange={(e) => handleFilterChange('difficulty', e.target.value)}
            className="filter-select"
          >
            <option value="all">All Difficulties</option>
            {difficulties.map((difficulty) => (
              <option key={difficulty} value={difficulty}>
                {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="sortBy" className="filter-label">Sort By</label>
          <select
            id="sortBy"
            value={filters.sortBy}
            onChange={(e) => handleFilterChange('sortBy', e.target.value)}
            className="filter-select"
          >
            <option value="name">Name (A-Z)</option>
            <option value="name-desc">Name (Z-A)</option>
            <option value="difficulty">Difficulty (Easy to Hard)</option>
            <option value="difficulty-desc">Difficulty (Hard to Easy)</option>
            <option value="category">Category</option>
            <option value="time">Estimated Time</option>
          </select>
        </div>
      </div>

      <div className="filter-actions">
        <button
          onClick={() => {
            const resetFilters = {
              search: '',
              category: 'all',
              difficulty: 'all',
              sortBy: 'name'
            };
            setFilters(resetFilters);
            onFilterChange(resetFilters);
          }}
          className="filter-reset"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
}
