import React from 'react';
import ReactDOM from 'react-dom';
import Weather from './weather';
import ApolloClient from "apollo-boost";
import { ApolloProvider } from "react-apollo";

const client = new ApolloClient({
  uri: 'http://127.0.0.1:4000/graphql'
});

const App = () => (
  <ApolloProvider client={client}>
    <Weather/>
  </ApolloProvider>
);

ReactDOM.render(<App />, document.getElementById("root"));


// ReactDOM.render(
//   <Dashboard />,
//   document.getElementById('root')
// );
