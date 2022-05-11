import VConsole from 'vconsole'
const vConsole = process.env.NODE_ENV === 'development' ? new VConsole() : ''

export default vConsole
