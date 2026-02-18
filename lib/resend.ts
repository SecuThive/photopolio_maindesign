import { Resend } from 'resend';

const apiKey = process.env.RESEND_API_KEY;

export const resend = apiKey ? new Resend(apiKey) : null;

export const isResendEnabled = Boolean(apiKey);

export const mailFrom =
  process.env.MAIL_FROM || 'UI Syntax <devthive@ui-syntax.com>';

export const mailReplyTo =
  process.env.MAIL_REPLY_TO || 'devthive@ui-syntax.com';
