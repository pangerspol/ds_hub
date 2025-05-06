import React, { useEffect, useMemo, useState } from 'react';
import { useTable, useSortBy, useFilters } from 'react-table';

function Dashboard() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

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

  const data = useMemo(() => records, [records]);

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
          <span className="text-sm mb-1">Filter by Provider</span>
          <input
            type="text"
            className="bg-gray-800 text-white border border-gray-700 rounded px-2 py-1"
            onChange={(e) => setFilter('provider_name', e.target.value || undefined)}
            placeholder="Type provider name"
          />
        </label>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="overflow-auto rounded shadow border border-gray-700">
          <table {...getTableProps()} className="min-w-full text-sm text-left">
            <thead className="bg-gray-800">
              {headerGroups.map(headerGroup => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                  {headerGroup.headers.map(col => (
                    <th {...col.getHeaderProps(col.getSortByToggleProps())} className="px-4 py-2 font-medium text-gray-300">
                      {col.render('Header')}
                      <span>{col.isSorted ? (col.isSortedDesc ? ' 🔽' : ' 🔼') : ''}</span>
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody {...getTableBodyProps()} className="divide-y divide-gray-800">
              {rows.map(row => {
                prepareRow(row);
                return (
                  <tr {...row.getRowProps()} className="hover:bg-gray-800">
                    {row.cells.map(cell => (
                      <td {...cell.getCellProps()} className="px-4 py-2 text-gray-200">
                        {cell.render('Cell')}
                      </td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;