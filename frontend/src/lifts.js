import React from 'react'
import { Query } from "react-apollo";
import gql from "graphql-tag";


const Lifts = () => (
  <Query
    query={gql`
      {
        lifts(id: 1) {
          name
          status_desc
        }
      }
    `}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;

      return data.lifts.map(({ name, status_desc }) => (
        <div key={name}>
          {name}: {status_desc}
        </div>
      ));
    }}
  </Query>
);


export default Lifts
