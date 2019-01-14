import { getResorts, getLifts, getResortsWithLifts } from '../resorts'
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

  }
};
// Exports
export default RESOLVERS;
