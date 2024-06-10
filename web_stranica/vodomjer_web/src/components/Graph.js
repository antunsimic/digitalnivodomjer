// src/LineChart.js
import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, elements } from 'chart.js';
import '../assets/graph.css'
// Register the components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Graph = ({ data }) => {
    const potrosnja = [];
    data.forEach((element) => {
        potrosnja.push(element.potrosnja);
    })

  const chartData = {
    labels: data.map((_, index) => `${_.datum}`),
    datasets: [
      {
        label: 'Potrošnja',
        data: potrosnja,
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: 'rgba(75,192,192,0.2)',
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Godišnja potrošnja',
      },
    },
  };

  return (
    <div className='graph'>
        <Line data={chartData} options={options} />
    </div>
  );
};

export default Graph;
