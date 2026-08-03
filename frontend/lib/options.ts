// Closed option sets for low-complexity wizard fields — chosen, not typed.

// Most frequent NIW origin countries first (per the approved-case DB),
// then the rest alphabetically.
const TOP_COUNTRIES = [
  "China", "India", "Iran", "Taiwan", "South Korea", "Turkey", "Brazil",
  "Egypt", "Nigeria", "Mexico", "Canada", "United Kingdom",
];

const OTHER_COUNTRIES = [
  "Afghanistan", "Albania", "Algeria", "Argentina", "Armenia", "Australia",
  "Austria", "Azerbaijan", "Bangladesh", "Belarus", "Belgium", "Bolivia",
  "Bosnia and Herzegovina", "Botswana", "Bulgaria", "Cambodia", "Cameroon",
  "Chile", "Colombia", "Costa Rica", "Croatia", "Cuba", "Cyprus",
  "Czech Republic", "Denmark", "Dominican Republic", "Ecuador",
  "El Salvador", "Estonia", "Ethiopia", "Finland", "France", "Georgia",
  "Germany", "Ghana", "Greece", "Guatemala", "Honduras", "Hong Kong",
  "Hungary", "Iceland", "Indonesia", "Iraq", "Ireland", "Israel", "Italy",
  "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kuwait",
  "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Libya", "Lithuania",
  "Macau", "Malaysia", "Mongolia", "Morocco", "Myanmar", "Nepal",
  "Netherlands", "New Zealand", "Nicaragua", "North Macedonia", "Norway",
  "Pakistan", "Panama", "Paraguay", "Peru", "Philippines", "Poland",
  "Portugal", "Qatar", "Romania", "Russia", "Saudi Arabia", "Serbia",
  "Singapore", "Slovakia", "Slovenia", "South Africa", "Spain",
  "Sri Lanka", "Sudan", "Sweden", "Switzerland", "Syria", "Tanzania",
  "Thailand", "Tunisia", "Uganda", "Ukraine", "United Arab Emirates",
  "United States", "Uruguay", "Uzbekistan", "Venezuela", "Vietnam",
  "Yemen", "Zambia", "Zimbabwe",
].filter((c) => !TOP_COUNTRIES.includes(c));

export const COUNTRIES = [...TOP_COUNTRIES, ...OTHER_COUNTRIES];

export const US_STATES = [
  "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI",
  "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN",
  "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
  "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
  "WV", "WI", "WY", "PR", "GU", "VI", "MP", "AS",
];

// MM/DD/YYYY (USCIS format, stored) <-> YYYY-MM-DD (native date input)
export function mdyToIso(v: string): string {
  const m = (v || "").match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  return m ? `${m[3]}-${m[1]}-${m[2]}` : "";
}
export function isoToMdy(v: string): string {
  const m = (v || "").match(/^(\d{4})-(\d{2})-(\d{2})$/);
  return m ? `${m[2]}/${m[3]}/${m[1]}` : "";
}
