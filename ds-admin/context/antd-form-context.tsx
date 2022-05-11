import { Form, FormInstance, FormProps } from 'antd'
import { createContext, useState } from 'react'

const { useForm } = Form

type AntdFromContextType<T = any> =
  | {
      form: FormInstance
      values: T
    }
  | undefined

export const AntdFromContext = createContext<AntdFromContextType>(undefined)

AntdFromContext.displayName = 'AntdFromContext'

export function AntdFormProvider<T>(props: FormProps<T>) {
  const [values, setValues] = useState<T>()
  const [form] = useForm()

  return (
    <AntdFromContext.Provider
      value={{
        form,
        values,
      }}
    >
      <Form form={form} onValuesChange={(_, v) => setValues(v)} {...props} />
    </AntdFromContext.Provider>
  )
}
