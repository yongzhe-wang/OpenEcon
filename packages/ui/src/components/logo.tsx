import { ComponentProps } from "solid-js"

export const Mark = (props: { class?: string }) => {
  return (
    <svg
      data-component="logo-mark"
      classList={{ [props.class ?? ""]: !!props.class }}
      viewBox="0 0 16 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path data-slot="logo-logo-mark-shadow" d="M12 10V12H4V10H12Z" fill="var(--icon-weak-base)" />
      <path
        data-slot="logo-logo-mark-e"
        d="M12 4H4V16H12V14H6V12H10V8H6V6H12V4ZM16 20H0V0H16V20Z"
        fill="var(--icon-strong-base)"
      />
    </svg>
  )
}

export const Splash = (props: Pick<ComponentProps<"svg">, "ref" | "class">) => {
  return (
    <svg
      ref={props.ref}
      data-component="logo-splash"
      classList={{ [props.class ?? ""]: !!props.class }}
      viewBox="0 0 80 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="M60 50V60H20V50H60Z" fill="var(--icon-base)" />
      <path d="M60 20H20V80H60V70H30V60H50V40H30V30H60V20ZM80 100H0V0H80V100Z" fill="var(--icon-strong-base)" />
    </svg>
  )
}

export const Logo = (props: { class?: string }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 234 42"
      fill="none"
      classList={{ [props.class ?? ""]: !!props.class }}
    >
      <g>
        <path d="M18 30H6V18H18V30Z" fill="var(--icon-weak-base)" />
        <path d="M18 12H6V30H18V12ZM24 36H0V6H24V36Z" fill="var(--icon-base)" />
        <path d="M48 30H36V18H48V30Z" fill="var(--icon-weak-base)" />
        <path d="M36 30H48V12H36V30ZM54 36H36V42H30V6H54V36Z" fill="var(--icon-base)" />
        <path d="M84 24V30H66V24H84Z" fill="var(--icon-weak-base)" />
        <path d="M84 24H66V30H84V36H60V6H84V24ZM66 18H78V12H66V18Z" fill="var(--icon-base)" />
        <path d="M108 36H96V18H108V36Z" fill="var(--icon-weak-base)" />
        <path d="M108 12H96V36H90V6H108V12ZM114 36H108V12H114V36Z" fill="var(--icon-base)" />
        <path d="M144 24V30H126V24H144Z" fill="var(--icon-weak-base)" />
        <path d="M144 24H126V30H144V36H120V6H144V24ZM126 18H138V12H126V18Z" fill="var(--icon-strong-base)" />
        <path d="M174 30H156V18H174V30Z" fill="var(--icon-weak-base)" />
        <path d="M174 12H156V30H174V36H150V6H174V12Z" fill="var(--icon-strong-base)" />
        <path d="M198 30H186V18H198V30Z" fill="var(--icon-weak-base)" />
        <path d="M198 12H186V30H198V12ZM204 36H180V6H204V36Z" fill="var(--icon-strong-base)" />
        <path d="M228 36H216V18H228V36Z" fill="var(--icon-weak-base)" />
        <path d="M228 12H216V36H210V6H228V12ZM234 36H228V12H234V36Z" fill="var(--icon-strong-base)" />
      </g>
    </svg>
  )
}
