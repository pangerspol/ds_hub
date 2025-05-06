import React, { useEffect, useMemo, useState } from 'react';
import { useTable, useSortBy, useFilters } from 'react-table';

function Dashboard() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(0);
  const [itemsPerPage, setItemsPerPage] = useState(200);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/entries/medical-records/', {
      credentials: 'include',
    })
      .then((res) => res.json())
      .then((data) => {
        setRecords(data);
        setLoading(false);
      });
  }, []);

  const filteredRecords = useMemo(() => {
    return records.filter((record) => {
      const lowerQuery = searchQuery.toLowerCase();
      return (
        record.client?.name?.toLowerCase().includes(lowerQuery) ||
        record.client?.case_number?.toLowerCase().includes(lowerQuery) ||
        record.provider?.name?.toLowerCase().includes(lowerQuery)
      );
    });
  }, [records, searchQuery]);

  const paginatedData = useMemo(() => {
    const start = currentPage * itemsPerPage;
    return filteredRecords.slice(start, start + itemsPerPage);
  }, [filteredRecords, currentPage, itemsPerPage]);

  const data = useMemo(() => paginatedData, [paginatedData]);

  const columns = useMemo(() => [
    {
      Header: 'Client Name',
      accessor: row => row.client?.name || '—',
      id: 'client_name'
    },
    {
      Header: 'Case Number',
      accessor: row => row.client?.case_number || '—',
      id: 'case_number'
    },
    {
      Header: 'Paralegal',
      accessor: row => row.client?.paralegal?.name || '—',
      id: 'paralegal'
    },
    {
      Header: 'Provider',
      accessor: row => row.provider?.name || '—',
      id: 'provider_name'
    },
    {
      Header: 'Facility',
      accessor: 'facility',
    },
    {
      Header: 'Invoice #',
      accessor: 'invoice_number',
    },
    {
      Header: 'Cost',
      accessor: 'cost',
      Cell: ({ value }) => value ? `$${parseFloat(value).toFixed(2)}` : '—',
    },
    {
      Header: 'Status',
      accessor: 'status',
      Cell: ({ value }) =>
        value
          .replace(/_/g, ' ')
          .replace(/\b\w/g, l => l.toUpperCase()),
    },
  ], []);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    setFilter,
  } = useTable({ columns, data }, useFilters, useSortBy);

  const totalPages = Math.ceil(filteredRecords.length / itemsPerPage);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Medical Records Dashboard</h1>

      <div className="flex flex-wrap gap-4">
        <label className="flex flex-col">
          <span className="text-sm mb-1">Filter by Status</span>
          <select
            className="bg-gray-800 text-white border border-gray-700 rounded px-2 py-1"
            onChange={(e) => setFilter('status', e.target.value || undefined)}
          >
            <option value="">All</option>
            <option value="new_entry">New Entry</option>
            <option value="pending_approval">Pending Approval</option>
            <option value="denied">Denied</option>
            <option value="pending_payment">Pending Payment</option>
            <option value="pending_records">Pending Records</option>
            <option value="completed">Completed</option>
          </select>
        </label>

        <label className="flex flex-col">
          <span className="text-sm mb-1">Record Search</span>
          <input
            type="text"
            className="bg-gray-800 text-white border border-gray-700 rounded px-2 py-1"
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setCurrentPage(0);
            }}
            placeholder="Search"
          />
        </label>

        <label className="flex flex-col">
          <span className="text-sm mb-1">Items per page</span>
          <select
            className="bg-gray-800 text-white border border-gray-700 rounded px-2 py-1"
            value={itemsPerPage}
            onChange={(e) => {
              setItemsPerPage(Number(e.target.value));
              setCurrentPage(0);
            }}
          >
            <option value={50}>50</option>
            <option value={100}>100</option>
            <option value={200}>200</option>
            <option value={500}>500</option>
          </select>
        </label>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <div className="overflow-auto rounded shadow border border-gray-700">
            <table {...getTableProps()} className="min-w-full text-sm text-left">
              <thead className="bg-gray-800">
                {headerGroups.map(headerGroup => {
                  const { key, ...rest } = headerGroup.getHeaderGroupProps();
                  return (
                    <tr key={key} {...rest}>
                      {headerGroup.headers.map(col => {
                        const { key: colKey, ...colRest } = col.getHeaderProps(col.getSortByToggleProps());
                        return (
                          <th key={colKey} {...colRest} className="px-4 py-2 font-medium text-gray-300">
                            {col.render('Header')}
                            <span>{col.isSorted ? (col.isSortedDesc ? ' 🔽' : ' 🔼') : ''}</span>
                          </th>
                        );
                      })}
                    </tr>
                  );
                })}
              </thead>
              <tbody {...getTableBodyProps()} className="divide-y divide-gray-800">
                {rows.map(row => {
                  prepareRow(row);
                  const { key, ...rowRest } = row.getRowProps();
                  return (
                    <tr key={key} {...rowRest} className="hover:bg-gray-800">
                      {row.cells.map(cell => {
                        const { key: cellKey, ...cellRest } = cell.getCellProps();
                        return (
                          <td key={cellKey} {...cellRest} className="px-4 py-2 text-gray-200">
                            {cell.render('Cell')}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="flex justify-between items-center mt-4">
            <button
              className="bg-gray-700 px-3 py-1 rounded disabled:opacity-50"
              disabled={currentPage === 0}
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 0))}
            >
              Previous
            </button>
            <span className="text-sm text-gray-400">
              Page {currentPage + 1} of {totalPages}
            </span>
            <button
              className="bg-gray-700 px-3 py-1 rounded disabled:opacity-50"
              disabled={currentPage >= totalPages - 1}
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages - 1))}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;