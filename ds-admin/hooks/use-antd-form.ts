import { FormInstance } from 'antd'
import { AntdFromContext } from 'context/antd-form-context'
import { useContext } from 'react'

export default function useAntdForm<T>() {
  const antdFrom = useContext(AntdFromContext)
  if (!antdFrom) {
    throw new Error('useAntdForm 必须在 AntdFromProvider 中使用')
  }

  return {
    values: antdFrom.values as T,
    form: antdFrom.form as FormInstance<T>,
  }
}
