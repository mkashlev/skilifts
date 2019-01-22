import React from 'react'
import { Query } from "react-apollo";
import gql from "graphql-tag";


const Lift = () => (
  <Query
    query={gql`
      {
        lift(id: 1) {
          name
          historical_status
        }
      }
    `}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;

      return (
        <div key={data.lift.name}>
          {data.lift.name}: {data.lift.historical_status}
        </div>
      );
    }}
  </Query>
);


export default Lift
