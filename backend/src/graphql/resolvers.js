import { getResorts, getLifts, getResortsWithLifts, getLift } from '../resorts'
// GraphQL: Resolvers
const RESOLVERS = {
  Query: {
    resorts: (parent, args) => {
      return getResorts()
    },
    lifts: (parent, args) => {
      return getLifts(args.id)
    },
    resortsWithLifts: (parent, args) => {
      return getResortsWithLifts()
    },
    lift: (parent, args) => {
      return getLift(args.id)
    }

  }
};
// Exports
export default RESOLVERS;
