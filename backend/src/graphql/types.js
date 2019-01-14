// Imports: GraphQL
import { gql } from 'apollo-server-express';
// GraphQL: TypeDefs
const TYPEDEFS = gql`
type Query {
  resorts: [Resort!]
  lifts(id: ID!): [Lift!]
  resortsWithLifts: [Resort!]
}
type Resort {
  id: ID
  name: String
  lifts: [Lift!]
}
type Lift {
  id: ID
  name: String
  status: Int
  resort_id: ID
}
`;
// Exports
export default TYPEDEFS;
