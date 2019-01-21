// Imports: GraphQL
import { gql } from 'apollo-server-express';
// GraphQL: TypeDefs
const TYPEDEFS = gql`
type Query {
  resorts: [Resort!]
  lifts(id: ID!): [Lift!]
  resortsWithLifts: [Resort!]
  lift(id: ID!): Lift
  weatherForResort(id: ID!, from: String, to: String): [Weather!]
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
type Weather {
  id: ID
  resort_id: ID
  source: String
  data_calculated_at: String
  label: String
  description: String
  temperature: String
  pressure: Int
  humidity: Int
  wind_speed: Float
  wind_dir: Float

}
`;
// Exports
export default TYPEDEFS;
