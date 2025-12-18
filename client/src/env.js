export function envFlag(name) {
  if (import.meta?.env) {
    return import.meta.env[`VITE_${name}`] === '1'
  } else {
    return process.env[`VUE_APP_${name}`] === '1'
  }
}
