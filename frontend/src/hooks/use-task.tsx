import toast from 'react-hot-toast';
import { isEmpty } from 'lodash-es';

import taskService, { TaskTypeEnums } from '@/api/task';
import { useUserStore } from '@/store';
import { useBillingStore } from '@/store';

const useTask = () => {
  const [isLogin] = useUserStore((state) => [state.isLogin()]);
  const [getCurrentBilling] = useBillingStore((state) => [state.getCurrentBilling]);

  // 分享成功
  async function shareCallback() {
    if (!isLogin) return;
    const type = TaskTypeEnums.SHARE;
    const { result } = await taskService.completionTask(type);
    if (!result) return;
    const unreadTask = await taskService.getUnreadTaskList(type);
    if (!isEmpty(unreadTask)) {
      // 修改记录为已读
      await taskService.readTask(type);
      getCurrentBilling();
      toast(() => (
        <div>
          <div className="bold text-lg">👏 今日分享已完成！</div>
          <div className="mt-4">
            {`${
              unreadTask.num === -1
                ? `Your conversation usage time will be extended${unreadTask.expired_day}sky`
                : `Your conversations will increase${unreadTask.num}Second-rate`
            }
                ，please go and use it`}
          </div>
        </div>
      ));
    }
  }

  async function checkTask(type: TaskTypeEnums) {
    if (!isLogin) return;
    const { result } = await taskService.checkTask(type);
    if (!result) return;
    const unreadTask = await taskService.getUnreadTaskList(type);
    if (!isEmpty(unreadTask)) {
      await taskService.readTask(type);
      getCurrentBilling();
      toast(() => (
        <div>
          <div className="bold text-lg">
            {type === TaskTypeEnums.REGISTER
              ? '👏 Welcome to join and enjoy it'
              : `👏 ${unreadTask.record_count}A friend joined, it’s really awesome!`}
          </div>
          {type === TaskTypeEnums.REGISTER ? (
            <div className="mt-4">
              {`You will have${
                unreadTask.num === -1
                  ? `${unreadTask.expired_day * unreadTask.record_count}Unlimited days`
                  : `${unreadTask.num * unreadTask.record_count}次`
              }Opportunity to talk to your assistant, please go and use it`}
            </div>
          ) : (
            <div className="mt-4">
              {`${
                unreadTask.num === -1
                  ? `+${unreadTask.expired_day * unreadTask.record_count}Conversation duration per day`
                  : `+${unreadTask.num * unreadTask.record_count}Conversations`
              }`}
            </div>
          )}
        </div>
      ));
    }
  }

  return {
    shareCallback,
    checkTask,
  };
};

export default useTask;
