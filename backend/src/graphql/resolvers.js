import { getResorts, getLifts, getResortsWithLifts, getLift } from '../resorts'
import { getWeatherForResort } from '../weather'
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
    },
    weatherForResort: (parent, args) => {
      return getWeatherForResort(args.id, args.from, args.to)
    },

  }
};
// Exports
export default RESOLVERS;
