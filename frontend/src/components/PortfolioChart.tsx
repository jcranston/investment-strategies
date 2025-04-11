import React from 'react'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend,
} from 'chart.js'
import { Line } from 'react-chartjs-2'

ChartJS.register(LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend)

interface PortfolioChartProps {
  data: { Date: string; Portfolio: number }[]
}

export default function PortfolioChart({ data }: PortfolioChartProps) {
  const labels = data.map(point => point.Date)
  const values = data.map(point => point.Portfolio)

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Portfolio Value ($)',
        data: values,
        fill: false,
        borderColor: 'rgb(37, 99, 235)', // Tailwind blue-600
        tension: 0.1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true },
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function (value: number) {
            return '$' + value.toLocaleString()
          },
        },
      },
    },
  }

  return (
    <div className="h-[400px] mt-8">
      <Line data={chartData} options={options} />
    </div>
  )
}
