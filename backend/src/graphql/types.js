// Imports: GraphQL
import { gql } from 'apollo-server-express';
// GraphQL: TypeDefs
const TYPEDEFS = gql`
type Query {
  resorts: [Resort!]
  lifts(id: ID!): [Lift!]
  resortsWithLifts: [Resort!]
  lift(id: ID!): Lift
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
  status_desc: String
  resort_id: ID
  historical_status: String
  updated_at: String
}
`;
// Exports
export default TYPEDEFS;
