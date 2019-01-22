import React from 'react'
import { Query } from "react-apollo";
import gql from "graphql-tag";
import { LineChart } from 'react-easy-chart';


const Weather = () => (
  <Query
    query={gql`
      {
        weatherForResort(id: 1, from: "2019-01-01 00:00:00") {
          temperature
        }
      }
    `}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;
      const temperatureData =  data.weatherForResort.map((weather, indx) => {
        return {x: indx+1, y: parseInt(weather.temperature) }
      })
      console.log(temperatureData)
      return (
        <LineChart
          width={1000}
          height={500}
          axes
          interpolate={'cardinal'}
          data={[temperatureData]}
        />
      )
    }}
  </Query>
);


export default Weather
