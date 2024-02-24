import { API_DOMAIN } from './request';
import { StoreKey } from '@/constants';
import { isEmpty } from 'lodash-es';

export enum StatusEnum {
  START = 'start',
  PENDING = 'pending',
  SUCCESS = 'success',
  ERROR = 'error',
  ABORT = 'abort',
}

interface StreamResponseType {
  messages: string;
  id: string;
}

type SendMessageType = {
  message: string;
  modelId?: string;
  requestId?: string;
  lastId?: string;
  onProgress: (_: StreamResponseType) => void;
  onFinish: (_: StreamResponseType) => void;
  onError: (_: string) => void;
};

export default class StreamAPI {
  private _status: string;
  constructor() {
    this._status = StatusEnum.START;
  }

  set status(status) {
    this._status = status;
  }

  get status() {
    return this._status;
  }

  abort() {
    this.status = StatusEnum.ABORT;
  }

  async send({ message, modelId, requestId, lastId, onProgress, onFinish, onError }: SendMessageType) {
    this.status = StatusEnum.START;
  
    try {
      // Generate a random timeout between 5 and 20 seconds
      const randomTimeout = Math.floor(Math.random() * (10 - 2 + 1) + 5) * 1000;
      
      // Simulate the request by setting a timeout
      await new Promise((resolve) => setTimeout(resolve, randomTimeout));
  
      if (this.status === StatusEnum.START) {
        this.status = StatusEnum.PENDING;
      }
      const mockResponse = {
      messages:"Hel",
      id: "1234567890"
    };
      const resChunkValue = mockResponse;
  
      if (this.status === StatusEnum.ABORT) {
        this.status = StatusEnum.SUCCESS;
        resChunkValue.messages = resChunkValue.messages + '\n[You have interrupted your answer. If you want to continue, please refresh and try again!]';
        onFinish(resChunkValue);
      }
  
      if (this.status === StatusEnum.PENDING || this.status === StatusEnum.SUCCESS) {
        this.status = StatusEnum.SUCCESS;
        if (isEmpty(resChunkValue)) {
          onError('No response data, please try again');
        } else {
          onFinish(resChunkValue);
        }
      }
    } catch (error) {
      onError('An error occurred, please try again');
      this.status = StatusEnum.ERROR;
    }
  }
}

export const streamAPI = new StreamAPI();
